import smtplib
import ssl
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests

import config

SENDGRID_MESSAGES_URL = "https://api.sendgrid.com/v3/mail/send"


def _build_verification_email(email: str, verify_url: str) -> MIMEMultipart:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Verify your email - DocAgent AI"
    msg["From"] = f"{config.SMTP_FROM_NAME} <{config.SMTP_FROM_EMAIL}>"
    msg["To"] = email

    text_body = (
        f"Welcome to DocAgent AI!\n\n"
        f"Please verify your email address by opening the link below:\n\n"
        f"{verify_url}\n\n"
        f"This link expires in 24 hours. If you did not create an account, "
        f"you can safely ignore this email.\n"
    )

    html_body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 520px; margin: 0 auto; padding: 32px; background: #f8fafc; border-radius: 12px;">
      <h2 style="color: #0f172a; margin-top: 0;">Verify your email</h2>
      <p style="color: #475569; font-size: 14px; line-height: 1.6;">
        Welcome to <strong>DocAgent AI</strong>! Please confirm your email address to activate your account.
      </p>
      <div style="text-align: center; margin: 28px 0;">
        <a href="{verify_url}"
           style="background: #0d9488; color: #ffffff; padding: 12px 28px; border-radius: 999px; text-decoration: none; font-weight: bold; font-size: 14px; display: inline-block;">
          Verify Email Address
        </a>
      </div>
      <p style="color: #94a3b8; font-size: 12px; line-height: 1.6;">
        This link expires in <strong>24 hours</strong>. If the button doesn't work, copy and paste this link into your browser:<br>
        <span style="color: #0d9488;">{verify_url}</span>
      </p>
      <p style="color: #94a3b8; font-size: 12px;">If you did not create an account, you can safely ignore this email.</p>
    </div>
    """

    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))
    return msg


def _send_via_sendgrid(email: str, first_name: str, confirmation_url: str) -> bool:
    """Send the verification email through the SendGrid v3 API using a dynamic template."""
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
                    "subject": config.SENDGRID_SUBJECT,
                },
            }
        ],
        "from": {
            "email": config.SENDGRID_FROM_EMAIL,
            "name": config.SENDGRID_FROM_NAME,
        },
        "template_id": config.SENDGRID_TEMPLATE_ID,
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
        print(f"[EmailService] Verification email sent to {email} via SendGrid")
        return True

    print(
        f"[EmailService] SendGrid error for {email}: "
        f"HTTP {response.status_code} {response.text}"
    )
    return False


def send_verification_email(email: str, token: str, first_name: str = "") -> bool:
    """Send a verification email. Returns True on success.

    Provider priority:
      1. SendGrid dynamic template (when SENDGRID_API_KEY + SENDGRID_TEMPLATE_ID are set)
      2. SMTP (when SMTP_HOST is set)
      3. Console print of the verification link (local development)
    """
    verify_url = f"{config.APP_BASE_URL}/api/auth/verify-email?token={token}"
    first_name = (first_name or "").strip()

    # 1. SendGrid (preferred)
    if config.SENDGRID_API_KEY and config.SENDGRID_TEMPLATE_ID:
        return _send_via_sendgrid(email, first_name, verify_url)

    # 2. SMTP fallback
    if config.SMTP_HOST and config.SMTP_FROM_EMAIL:
        msg = _build_verification_email(email, verify_url)
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
