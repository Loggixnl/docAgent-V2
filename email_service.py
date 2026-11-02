import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config


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


def send_verification_email(email: str, token: str) -> bool:
    """Send a verification email. Returns True on success.

    If SMTP is not configured, the verification link is printed to the
    server console instead so local development still works.
    """
    verify_url = f"{config.APP_BASE_URL}/api/auth/verify-email?token={token}"

    if not config.SMTP_HOST or not config.SMTP_FROM_EMAIL:
        print(f"[EmailService] SMTP not configured. Verification link for {email}:\n  {verify_url}")
        return True

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
