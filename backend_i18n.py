"""Backend string catalog for English (en) and Dutch (nl).

Used for verification emails, auth API errors, the email-verification page,
canned chat replies, and widget inquiry errors.
"""

MESSAGES = {
    "en": {
        # --- Verification email (SMTP fallback) ---
        "email.subject": "Verify your email - DocAgent AI",
        "email.heading": "Verify your email",
        "email.welcome_html": (
            "Welcome to <strong>DocAgent AI</strong>! Please confirm your email "
            "address to activate your account."
        ),
        "email.button": "Verify Email Address",
        "email.expiry_html": (
            "This link expires in <strong>24 hours</strong>. If the button doesn't "
            "work, copy and paste this link into your browser:<br>"
            '<span style="color: #0d9488;">{url}</span>'
        ),
        "email.ignore_html": "If you did not create an account, you can safely ignore this email.",
        "email.text": (
            "Welcome to DocAgent AI!\n\n"
            "Please verify your email address by opening the link below:\n\n"
            "{url}\n\n"
            "This link expires in 24 hours. If you did not create an account, "
            "you can safely ignore this email.\n"
        ),
        # --- Password reset email (SMTP / plain SendGrid) ---
        "email.reset_subject": "Reset your password - DocAgent AI",
        "email.reset_heading": "Reset your password",
        "email.reset_welcome_html": (
            "We received a request to reset the password for your "
            "<strong>DocAgent AI</strong> account."
        ),
        "email.reset_button": "Reset Password",
        "email.reset_expiry_html": (
            "This link expires in <strong>30 minutes</strong>. If the button doesn't "
            "work, copy and paste this link into your browser:<br>"
            '<span style="color: #0d9488;">{url}</span>'
        ),
        "email.reset_ignore_html": (
            "If you did not request a password reset, you can safely ignore this email. "
            "Your password will not change."
        ),
        "email.reset_text": (
            "DocAgent AI - password reset\n\n"
            "Open the link below to choose a new password:\n\n"
            "{url}\n\n"
            "This link expires in 30 minutes. If you did not request a password reset, "
            "you can safely ignore this email.\n"
        ),
        # --- Auth API errors ---
        "auth.invalid_email": "Invalid email address format.",
        "auth.password_short": "Password must be at least 4 characters long.",
        "auth.password_mismatch": "Passwords do not match.",
        "auth.already_registered": "This email is already registered. Please log in.",
        "auth.pending_resent": "This email is awaiting verification. A new verification email has been sent.",
        "auth.pending_resent_signup": "This signup is awaiting email verification. A new verification email has been sent.",
        "auth.almost_done": "Almost done! Please check your email and verify your account to activate it.",
        "auth.signup_failed": "Failed to create signup request: {error}",
        "auth.invalid_credentials": "Invalid email or password.",
        "auth.not_verified": "Email not verified. Please check your inbox for the verification link, or resend it.",
        "auth.resend_generic": "If an unverified account exists for this email, a verification link has been sent.",
        "auth.forgot_generic": "If an account exists for this email, a password reset link has been sent.",
        "auth.reset_invalid_link": "Invalid or already-used password reset link.",
        "auth.reset_expired": "This password reset link has expired. Please request a new one.",
        "auth.reset_success": "Your password has been reset. You can now log in with your new password.",
        # --- Verification landing page ---
        "verify.title": "Email Verification - DocAgent AI",
        "verify.success_heading": "Email Verified",
        "verify.failure_heading": "Verification Failed",
        "verify.go_to_login": "Go to Login",
        "verify.resend_hint": (
            'Return to the app and use <strong>"Resend verification email"</strong> '
            "to get a new link."
        ),
    "verify.success_message": "Your email has been verified! You can now log in to your account.",
    "verify.invalid_link": "Invalid or already-used verification link.",
    "verify.expired": "This verification link has expired. Please request a new one.",
        # --- Chat ---
        "chat.greeting": (
    "Hey there! 👋 I'm **DocAgent AI**. "
    "I'm here to make things easier by helping you find answers and get the information you need.\n\n"
    "Feel free to ask me anything!"
),
        "chat.identity": (
            "I am **DocAgent AI**, a specialized Knowledge Base AI Assistant. "
            "My role is to answer questions strictly and solely from the documents you upload.\n\n"
            "I do not answer questions using external general knowledge. "
            "Please upload documents and ask questions regarding their content."
        ),
        "chat.gratitude": (
            "You're very welcome! If you have any further questions about your uploaded documents, "
            "feel free to ask."
        ),
        "chat.refusal": (
            "I couldn't find a relevant answer to your query. "
            "Please contact the Administration or Support team for further assistance."
        ),
        "chat.decline": (
            "I couldn't find anything for your query in the uploaded documents. "
            "You can raise your query to Administration/Support."
        ),
        "chat.no_documents": (
            "No documents have been uploaded yet. Please upload your documents first so I can "
            "answer questions based strictly on their content."
        ),
        "chat.api_key_missing": (
            "AI API key is not configured on the server. Please set an API key in the server .env file."
        ),
        "chat.language_rule": "LANGUAGE RULE: Always respond in English.",
        # --- Widget inquiry ---
        "widget.chatbot_not_found": "Chatbot instance not found.",
        "widget.title_required": "Please provide a title for your inquiry.",
        "widget.description_required": "Please provide a description for your inquiry.",
        "widget.submit_failed": "Failed to submit inquiry: {error}",
    },
    "nl": {
        # --- Verification email (SMTP fallback) ---
        "email.subject": "Verifieer je e-mail - DocAgent AI",
        "email.heading": "Verifieer je e-mail",
        "email.welcome_html": (
            "Welkom bij <strong>DocAgent AI</strong>! Bevestig je e-mailadres om "
            "je account te activeren."
        ),
        "email.button": "E-mailadres verifiëren",
        "email.expiry_html": (
            "Deze link verloopt over <strong>24 uur</strong>. Werkt de knop niet? "
            "Kopieer en plak deze link in je browser:<br>"
            '<span style="color: #0d9488;">{url}</span>'
        ),
        "email.ignore_html": "Als je geen account hebt aangemaakt, kun je deze e-mail negeren.",
        "email.text": (
            "Welkom bij DocAgent AI!\n\n"
            "Verifieer je e-mailadres door de link hieronder te openen:\n\n"
            "{url}\n\n"
            "Deze link verloopt over 24 uur. Als je geen account hebt aangemaakt, "
            "kun je deze e-mail veilig negeren.\n"
        ),
        # --- Password reset email (SMTP / plain SendGrid) ---
        "email.reset_subject": "Wachtwoord opnieuw instellen - DocAgent AI",
        "email.reset_heading": "Wachtwoord opnieuw instellen",
        "email.reset_welcome_html": (
            "We hebben een verzoek ontvangen om het wachtwoord van je "
            "<strong>DocAgent AI</strong>-account opnieuw in te stellen."
        ),
        "email.reset_button": "Wachtwoord opnieuw instellen",
        "email.reset_expiry_html": (
            "Deze link verloopt over <strong>30 minuten</strong>. Werkt de knop niet? "
            "Kopieer en plak deze link in je browser:<br>"
            '<span style="color: #0d9488;">{url}</span>'
        ),
        "email.reset_ignore_html": (
            "Als je geen wachtwoordreset hebt aangevraagd, kun je deze e-mail veilig "
            "negeren. Je wachtwoord wordt niet gewijzigd."
        ),
        "email.reset_text": (
            "DocAgent AI - wachtwoord opnieuw instellen\n\n"
            "Open de link hieronder om een nieuw wachtwoord te kiezen:\n\n"
            "{url}\n\n"
            "Deze link verloopt over 30 minuten. Als je geen wachtwoordreset hebt "
            "aangevraagd, kun je deze e-mail veilig negeren.\n"
        ),
        # --- Auth API errors ---
        "auth.invalid_email": "Ongeldig e-mailadresformaat.",
        "auth.password_short": "Wachtwoord moet minstens 4 tekens lang zijn.",
        "auth.password_mismatch": "Wachtwoorden komen niet overeen.",
        "auth.already_registered": "Dit e-mailadres is al geregistreerd. Log in.",
        "auth.pending_resent": "Dit e-mailadres wacht op verificatie. Er is een nieuwe verificatie-e-mail verstuurd.",
        "auth.pending_resent_signup": "Deze registratie wacht op e-mailverificatie. Er is een nieuwe verificatie-e-mail verstuurd.",
        "auth.almost_done": "Bijna klaar! Controleer je e-mail en verifieer je account om deze te activeren.",
        "auth.signup_failed": "Registratie mislukt: {error}",
        "auth.invalid_credentials": "Ongeldig e-mailadres of wachtwoord.",
        "auth.not_verified": "E-mail niet geverifieerd. Controleer je inbox op de verificatielink, of stuur de e-mail opnieuw.",
        "auth.resend_generic": "Als er een niet-geverifieerd account bestaat voor dit e-mailadres, is er een verificatielink verstuurd.",
        "auth.forgot_generic": "Als er een account bestaat voor dit e-mailadres, is er een wachtwoordresetlink verstuurd.",
        "auth.reset_invalid_link": "Ongeldige of al gebruikte wachtwoordresetlink.",
        "auth.reset_expired": "Deze wachtwoordresetlink is verlopen. Vraag een nieuwe aan.",
        "auth.reset_success": "Je wachtwoord is opnieuw ingesteld. Je kunt nu inloggen met je nieuwe wachtwoord.",
        # --- Verification landing page ---
        "verify.title": "E-mailverificatie - DocAgent AI",
        "verify.success_heading": "E-mail geverifieerd",
        "verify.failure_heading": "Verificatie mislukt",
        "verify.go_to_login": "Ga naar inloggen",
        "verify.resend_hint": (
            'Ga terug naar de app en gebruik <strong>"Verificatie-e-mail opnieuw sturen"</strong> '
            "om een nieuwe link te krijgen."
        ),
    "verify.success_message": "Je e-mail is geverifieerd! Je kunt nu inloggen op je account.",
    "verify.invalid_link": "Ongeldige of al gebruikte verificatielink.",
    "verify.expired": "Deze verificatielink is verlopen. Vraag een nieuwe aan.",
        # --- Chat ---
        "chat.greeting": (
            "Hallo! Ik ben **DocAgent AI**, jouw assistent voor documentkennisbanken. "
            "Ik beantwoord vragen uitsluitend op basis van je geüploade documenten.\n\n"
            "Stel gerust een vraag over je geüploade documenten, dan zoek ik het antwoord voor je uit."
        ),
        "chat.identity": (
            "Ik ben **DocAgent AI**, een gespecialiseerde kennisbank-assistent. "
            "Mijn rol is om vragen strikt en uitsluitend te beantwoorden op basis van de documenten die je uploadt.\n\n"
            "Ik beantwoord geen vragen met algemene kennis van buitenaf. "
            "Upload documenten en stel vragen over hun inhoud."
        ),
        "chat.gratitude": (
            "Graag gedaan! Als je nog meer vragen hebt over je geüploade documenten, "
            "stel ze gerust."
        ),
        "chat.refusal": (
            "Ik kon geen relevant antwoord op je vraag vinden. "
            "Neem contact op met de beheer- of ondersteuningsploeg voor verdere hulp."
        ),
        "chat.decline": (
            "Ik kon niets vinden voor je vraag in de geüploade documenten. "
            "Je kunt je vraag voorleggen aan Beheer/Support."
        ),
        "chat.no_documents": (
            "Er zijn nog geen documenten geüpload. Upload eerst je documenten zodat ik "
            "vragen strikt op basis van hun inhoud kan beantwoorden."
        ),
        "chat.api_key_missing": (
            "De AI-API-sleutel is niet ingesteld op de server. Stel een API-sleutel in het .env-bestand van de server in."
        ),
        "chat.language_rule": "TAALREGEL: Antwoord altijd in het Nederlands.",
        # --- Widget inquiry ---
        "widget.chatbot_not_found": "Chatbot-instance niet gevonden.",
        "widget.title_required": "Geef een titel op voor je aanvraag.",
        "widget.description_required": "Geef een beschrijving op voor je aanvraag.",
        "widget.submit_failed": "Aanvraag indienen mislukt: {error}",
    },
}


def normalize_lang(lang) -> str:
    """Return a supported language code ('en' | 'nl'), defaulting to 'en'."""
    try:
        code = (lang or "").strip().lower()
    except Exception:
        code = ""
    return code if code in MESSAGES else "en"


def msg(lang, key, **kwargs) -> str:
    """Look up a localized string. Falls back to English, then to the key."""
    code = normalize_lang(lang)
    template = MESSAGES[code].get(key) or MESSAGES["en"].get(key) or key
    if kwargs:
        try:
            return template.format(**kwargs)
        except Exception:
            return template
    return template
