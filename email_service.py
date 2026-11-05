import smtplib
import ssl
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests

import backend_i18n
import config

SENDGRID_MESSAGES_URL = "https://api.sendgrid.com/v3/mail/send"


def _build_verification_email(email: str, verify_url: str, lang: str = "en") -> MIMEMultipart:
    lang = backend_i18n.normalize_lang(lang)
    msg = MIMEMultipart("alternative")
    msg["Subject"] = backend_i18n.msg(lang, "email.subject")
    msg["From"] = f"{config.SMTP_FROM_NAME} <{config.SMTP_FROM_EMAIL}>"
    msg["To"] = email

    text_body = backend_i18n.msg(lang, "email.text", url=verify_url)

    html_body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 520px; margin: 0 auto; padding: 32px; background: #f8fafc; border-radius: 12px;">
      <h2 style="color: #0f172a; margin-top: 0;">{backend_i18n.msg(lang, "email.heading")}</h2>
      <p style="color: #475569; font-size: 14px; line-height: 1.6;">
        {backend_i18n.msg(lang, "email.welcome_html")}
      </p>
      <div style="text-align: center; margin: 28px 0;">
        <a href="{verify_url}"
           style="background: #0d9488; color: #ffffff; padding: 12px 28px; border-radius: 999px; text-decoration: none; font-weight: bold; font-size: 14px; display: inline-block;">
          {backend_i18n.msg(lang, "email.button")}
        </a>
      </div>
      <p style="color: #94a3b8; font-size: 12px; line-height: 1.6;">
        {backend_i18n.msg(lang, "email.expiry_html", url=verify_url)}
      </p>
      <p style="color: #94a3b8; font-size: 12px;">{backend_i18n.msg(lang, "email.ignore_html")}</p>
    </div>
    """

    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))
    return msg


def _send_via_sendgrid(email: str, first_name: str, confirmation_url: str, lang: str = "en") -> bool:
    """Send the verification email through the SendGrid v3 API using a dynamic template."""
    lang = backend_i18n.normalize_lang(lang)
    template_id = config.SENDGRID_TEMPLATE_ID
    subject = config.SENDGRID_SUBJECT
    if lang == "nl":
        if config.SENDGRID_TEMPLATE_ID_NL:
            template_id = config.SENDGRID_TEMPLATE_ID_NL
            subject = config.SENDGRID_SUBJECT_NL or subject
        else:
            print(
                "[EmailService] SENDGRID_TEMPLATE_ID_NL is not set — "
                f"falling back to the English template for {email}"
            )

    headers = {
        "Authorization": f"Bearer {config.SENDGRID_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "personalizations": [
            {
                "to": [
                    {
                        "email": email,
                        "name": first_name or email.split("@")[0],
                    }
                ],
                "dynamic_template_data": {
                    "first_name": first_name,
                    "confirmation_url": confirmation_url,
                    "expiry_hours": 24,
                    "year": datetime.now().year,
                    "subject": subject,
                    "lang": lang,
                },
            }
        ],
        "from": {
            "email": config.SENDGRID_FROM_EMAIL,
            "name": config.SENDGRID_FROM_NAME,
        },
        "template_id": template_id,
    }

    try:
        response = requests.post(
            SENDGRID_MESSAGES_URL,
            headers=headers,
            json=payload,
            timeout=15,
        )
    except Exception as e:
        print(f"[EmailService] SendGrid request failed for {email}: {e}")
        return False

    if response.status_code == 202:
        print(
            f"[EmailService] Verification email sent to {email} via SendGrid "
            f"(lang={lang}, template={template_id})"
        )
        return True

    print(
        f"[EmailService] SendGrid error for {email}: "
        f"HTTP {response.status_code} {response.text}"
    )
    return False


def send_verification_email(email: str, token: str, first_name: str = "", lang: str = "en") -> bool:
    """Send a verification email in the given language. Returns True on success.

    Provider priority:
      1. SendGrid dynamic template (when SENDGRID_API_KEY + SENDGRID_TEMPLATE_ID are set)
      2. SMTP (when SMTP_HOST is set)
      3. Console print of the verification link (local development)
    """
    lang = backend_i18n.normalize_lang(lang)
    # Confirmation link points at the frontend origin, served by the SPA fallback /
    # preview proxy which forwards /api to the backend. Browser GETs render the
    # verification HTML page; the SPA also reads ?verify_token= as a fallback.
    verify_url = f"{config.APP_FRONTEND_URL}/api/auth/verify-email?token={token}&lang={lang}"
    first_name = (first_name or "").strip()

    # 1. SendGrid (preferred)
    if config.SENDGRID_API_KEY and config.SENDGRID_TEMPLATE_ID:
        return _send_via_sendgrid(email, first_name, verify_url, lang)

    # 2. SMTP fallback
    if config.SMTP_HOST and config.SMTP_FROM_EMAIL:
        msg = _build_verification_email(email, verify_url, lang)
        try:
            if config.SMTP_USE_SSL:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(config.SMTP_HOST, config.SMTP_PORT, context=context, timeout=30) as server:
                    if config.SMTP_USERNAME:
                        server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
                    server.sendmail(config.SMTP_FROM_EMAIL, [email], msg.as_string())
            else:
                with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT, timeout=30) as server:
                    if config.SMTP_USE_TLS:
                        context = ssl.create_default_context()
                        server.starttls(context=context)
                    if config.SMTP_USERNAME:
                        server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
                    server.sendmail(config.SMTP_FROM_EMAIL, [email], msg.as_string())
            print(f"[EmailService] Verification email sent to {email}")
            return True
        except Exception as e:
            print(f"[EmailService] Failed to send verification email to {email}: {e}")
            return False

    # 3. No provider configured: print the link so local development still works.
    print(f"[EmailService] No email provider configured. Verification link for {email}:\n  {verify_url}")
    return True
