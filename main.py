import os
import uuid
import shutil
import hashlib
import secrets
import re
import time
from datetime import datetime, timedelta
from fastapi import FastAPI, UploadFile, File, Form, Header, HTTPException, Depends, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse, Response
from pydantic import BaseModel
from typing import List, Optional

import config
import backend_i18n
from vector_store import VectorStore
import document_processor
import ai_agent
import email_service

# Initialize FastAPI App
app = FastAPI(
    title="AI Policy & Employee Handbook Assistant API",
    description="Backend API for vector-indexing HR documents and answering natural language policy queries."
)

# Enable CORS for cross-origin frontend requests
if config.CORS_ALLOW_ALL:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ORIGINS,
        allow_origin_regex=config.CORS_ORIGIN_REGEX,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# The embeddable widget is served from arbitrary customer websites, so its
# public endpoints must accept any origin. Registered after CORSMiddleware
# so it runs first (outermost) and handles those preflights itself.
WIDGET_PUBLIC_PATH_PREFIXES = ("/api/chat", "/api/widget/")

@app.middleware("http")
async def widget_public_cors(request: Request, call_next):
    origin = request.headers.get("origin")
    path = request.url.path
    if not origin or not any(path.startswith(p) for p in WIDGET_PUBLIC_PATH_PREFIXES):
        return await call_next(request)

    if request.method == "OPTIONS":
        return Response(
            status_code=204,
            headers={
                "Access-Control-Allow-Origin": origin,
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": request.headers.get("access-control-request-headers", "*"),
                "Access-Control-Max-Age": "86400",
                "Vary": "Origin",
            },
        )

    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Vary"] = "Origin"
    return response
# Initialize SQLite database
vector_db = VectorStore()

# Track app start time for uptime reporting
APP_START_TIME = time.time()

# Pydantic Schemas
class ChatMessage(BaseModel):
    role: str
    text: str

class ChatRequest(BaseModel):
    query: str
    chat_history: Optional[List[ChatMessage]] = []
    model: Optional[str] = None
    provider: Optional[str] = None  # gemini, openai, claude, generic, groq, openrouter
    chatbot_id: Optional[str] = "default"
    session_id: Optional[str] = None
    save_session: Optional[bool] = True
    base_url: Optional[str] = None
    lang: Optional[str] = "en"  # en | nl

class SettingsRequest(BaseModel):
    api_key: Optional[str] = ""
    provider: Optional[str] = None
    gemini_key: Optional[str] = None
    openai_key: Optional[str] = None
    claude_key: Optional[str] = None
    generic_key: Optional[str] = None
    generic_base_url: Optional[str] = None
    generic_model: Optional[str] = None


class AuthRequest(BaseModel):
    email: str
    password: str = ""
    lang: Optional[str] = "en"  # en | nl

class RegisterRequest(BaseModel):
    email: str
    password: str
    confirm_password: str
    first_name: str = ""
    lang: Optional[str] = "en"  # en | nl

class AdminQuestionUpdate(BaseModel):
    status: Optional[str] = None
    admin_response: Optional[str] = None

class WidgetInquiryRequest(BaseModel):
    chatbot_id: str
    email: str
    title: str
    description: str
    lang: Optional[str] = "en"  # en | nl

class ForgotPasswordRequest(BaseModel):
    email: str
    lang: Optional[str] = "en"  # en | nl

class ResetPasswordRequest(BaseModel):
    token: str
    password: str
    confirm_password: str
    lang: Optional[str] = "en"  # en | nl

# Password hashing helpers
def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt.hex() + ":" + key.hex()

def verify_password(password: str, hashed: str) -> bool:
    try:
        salt_hex, key_hex = hashed.split(":")
        salt = bytes.fromhex(salt_hex)
        key = bytes.fromhex(key_hex)
        new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return secrets.compare_digest(key, new_key)
    except Exception:
        return False

# Email format check
def is_valid_email(email: str) -> bool:
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(regex, email))

# Auth Dependency
async def get_current_user(
    authorization: Optional[str] = Header(None),
    x_session_token: Optional[str] = Header(None)
):
    token = None
    if x_session_token:
        token = x_session_token
    elif authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        
    if not token:
        raise HTTPException(status_code=401, detail="Authentication session token required.")
        
    session = vector_db.get_session(token)
    if not session:
        raise HTTPException(status_code=401, detail="Session expired or invalid.")
        
    try:
        expires_at = datetime.fromisoformat(session["expires_at"])
        if datetime.now() > expires_at:
            vector_db.delete_session(token)
            raise HTTPException(status_code=401, detail="Session expired.")
    except Exception:
        pass
        
    return session

# Health Check Endpoint

@app.get("/api/health")
def health_check():
    """Public health check endpoint. Returns overall status and component checks."""
    components = {}
    overall_status = "healthy"

    # Check database connectivity
    try:
        conn = vector_db._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        conn.close()
        components["database"] = {
            "status": "healthy",
            "engine": "postgresql" if vector_db.is_postgres else "sqlite"
        }
    except Exception as e:
        components["database"] = {"status": "unhealthy", "error": str(e)}
        overall_status = "unhealthy"

    # Check upload directory exists and is writable
    try:
        upload_dir = config.UPLOAD_DIR
        os.makedirs(upload_dir, exist_ok=True)
        test_path = os.path.join(upload_dir, ".healthcheck")
        with open(test_path, "w") as f:
            f.write("ok")
        os.remove(test_path)
        components["storage"] = {"status": "healthy", "path": upload_dir}
    except Exception as e:
        components["storage"] = {"status": "unhealthy", "error": str(e)}
        overall_status = "unhealthy"

    # Check at least one AI provider key is configured
    try:
        configured = [
            name for name, key in {
                "gemini": config.GEMINI_API_KEY,
                "openai": config.OPENAI_API_KEY,
                "claude": config.CLAUDE_API_KEY,
                "generic": config.GENERIC_API_KEY,
            }.items() if key
        ]
        if configured:
            components["ai_providers"] = {"status": "healthy", "configured": configured}
        else:
            components["ai_providers"] = {"status": "degraded", "configured": [], "note": "No AI provider API keys configured."}
            if overall_status == "healthy":
                overall_status = "degraded"
    except Exception as e:
        components["ai_providers"] = {"status": "unhealthy", "error": str(e)}
        overall_status = "unhealthy"

    response = {
        "status": overall_status,
        "uptime_seconds": round(time.time() - APP_START_TIME, 2),
        "timestamp": datetime.now().isoformat(),
        "components": components
    }

    status_code = 200 if overall_status in ("healthy", "degraded") else 503
    return JSONResponse(content=response, status_code=status_code)

# Auth Endpoints

@app.post("/api/auth/register")
def register_user(request: RegisterRequest):
    email = request.email.strip().lower()
    password = request.password
    confirm_password = request.confirm_password
    first_name = request.first_name.strip()
    lang = backend_i18n.normalize_lang(request.lang)
    
    if not is_valid_email(email):
        raise HTTPException(status_code=400, detail=backend_i18n.msg(lang, "auth.invalid_email"))
        
    if len(password) < 4:
        raise HTTPException(status_code=400, detail=backend_i18n.msg(lang, "auth.password_short"))
        
    if password != confirm_password:
        raise HTTPException(status_code=400, detail=backend_i18n.msg(lang, "auth.password_mismatch"))
        
    existing_user = vector_db.get_user_by_email(email)
    if existing_user:
        if existing_user.get("email_verified"):
            raise HTTPException(status_code=400, detail=backend_i18n.msg(lang, "auth.already_registered"))
        # Legacy unverified account (created before deferred signup): refresh and resend
        verify_token = secrets.token_urlsafe(32)
        token_expires = (datetime.now() + timedelta(hours=24)).isoformat()
        vector_db.set_user_verification_token(email, verify_token, token_expires)
        email_service.send_verification_email(email, verify_token, existing_user.get("first_name", ""), lang)
        return {
            "success": True,
            "email": email,
            "requires_verification": True,
            "message": backend_i18n.msg(lang, "auth.pending_resent")
        }

    pending = vector_db.get_pending_registration(email)
    verify_token = secrets.token_urlsafe(32)
    token_expires = (datetime.now() + timedelta(hours=24)).isoformat()

    if pending:
        # Signup already awaiting verification: refresh the token and resend
        vector_db.set_pending_verification_token(email, verify_token, token_expires)
        email_service.send_verification_email(email, verify_token, pending.get("first_name", ""), lang)
        return {
            "success": True,
            "email": email,
            "requires_verification": True,
            "message": backend_i18n.msg(lang, "auth.pending_resent_signup")
        }

    user_id = str(uuid.uuid4())
    chatbot_id = "cb_" + secrets.token_hex(6)
    password_hash = hash_password(password)

    # No account is created yet — only a pending signup. The users row is created
    # when the verification link is clicked (promote_pending_registration).
    try:
        vector_db.save_pending_registration(
            email, user_id, chatbot_id, first_name,
            password_hash, verify_token, token_expires
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=backend_i18n.msg(lang, "auth.signup_failed", error=str(e))
        )

    email_service.send_verification_email(email, verify_token, first_name, lang)

    return {
        "success": True,
        "email": email,
        "requires_verification": True,
        "message": backend_i18n.msg(lang, "auth.almost_done")
    }

@app.post("/api/auth/login")
def login_user(request: AuthRequest):
    email = request.email.strip().lower()
    password = request.password
    lang = backend_i18n.normalize_lang(request.lang)
    
    user = vector_db.get_user_by_email(email)
    if not user:
        # No account yet — but a signup may be awaiting email verification
        if vector_db.get_pending_registration(email):
            raise HTTPException(
                status_code=403,
                detail=backend_i18n.msg(lang, "auth.not_verified")
            )
        raise HTTPException(status_code=401, detail=backend_i18n.msg(lang, "auth.invalid_credentials"))

    if not verify_password(password, user["password_hash"]):
        raise HTTPException(status_code=401, detail=backend_i18n.msg(lang, "auth.invalid_credentials"))

    if not user.get("email_verified"):
        raise HTTPException(
            status_code=403,
            detail=backend_i18n.msg(lang, "auth.not_verified")
        )

    token = secrets.token_hex(24)
    expires_at = (datetime.now() + timedelta(days=30)).isoformat()
    vector_db.create_session(token, user["id"], user["chatbot_id"], expires_at)
    
    return {
        "success": True,
        "token": token,
        "email": user["email"],
        "chatbot_id": user["chatbot_id"]
    }

@app.get("/api/auth/verify-email")
def verify_email(request: Request, token: str, lang: str = "en"):
    """Verify an email address from the link in the verification email.

    Returns JSON when the caller sends Accept: application/json (the frontend SPA),
    otherwise renders a simple server-side HTML page for direct browser hits.
    """
    lang = backend_i18n.normalize_lang(lang)
    wants_json = "application/json" in (request.headers.get("accept") or "")

    def fail(message: str):
        if wants_json:
            return JSONResponse(
                {"success": False, "message": message, "lang": lang},
                status_code=400,
            )
        return _verification_page(False, message, lang=lang)

    try:
        # Normal path: promote a pending signup to a real account
        user = vector_db.promote_pending_registration(token)
        # Legacy path: token issued to a pre-existing users row
        if not user:
            user = vector_db.verify_user_by_token(token)
    except ValueError as e:
        # Localize the hardcoded expiry error from the DB layer
        message = (
            backend_i18n.msg(lang, "verify.expired")
            if "expired" in str(e).lower()
            else str(e)
        )
        return fail(message)

    if not user:
        return fail(backend_i18n.msg(lang, "verify.invalid_link"))

    message = backend_i18n.msg(lang, "verify.success_message")
    if wants_json:
        return {"success": True, "message": message, "lang": lang}
    return _verification_page(
        True,
        message,
        login_url=f"{config.APP_FRONTEND_URL}/?lang={lang}",
        lang=lang,
    )

@app.post("/api/auth/resend-verification")
def resend_verification(request: AuthRequest):
    """Resend the verification email for an existing unverified account."""
    email = request.email.strip().lower()
    lang = backend_i18n.normalize_lang(request.lang)

    # Return the same response whether the account exists or not, to avoid email enumeration.
    generic_response = {
        "success": True,
        "message": backend_i18n.msg(lang, "auth.resend_generic")
    }

    # Signup awaiting verification (no users row yet)
    pending = vector_db.get_pending_registration(email)
    if pending:
        verify_token = secrets.token_urlsafe(32)
        token_expires = (datetime.now() + timedelta(hours=24)).isoformat()
        vector_db.set_pending_verification_token(email, verify_token, token_expires)
        email_service.send_verification_email(email, verify_token, pending.get("first_name", ""), lang)
        return generic_response

    # Legacy unverified users row
    user = vector_db.get_user_by_email(email)
    if not user or user.get("email_verified"):
        return generic_response

    verify_token = secrets.token_urlsafe(32)
    token_expires = (datetime.now() + timedelta(hours=24)).isoformat()
    vector_db.set_user_verification_token(email, verify_token, token_expires)
    email_service.send_verification_email(email, verify_token, user.get("first_name", ""), lang)

    return generic_response

@app.post("/api/auth/forgot-password")
def forgot_password(request: ForgotPasswordRequest):
    """Send a password reset link for an existing, verified account.

    Always returns the same generic message so this endpoint cannot be used
    to discover which email addresses are registered.
    """
    email = request.email.strip().lower()
    lang = backend_i18n.normalize_lang(request.lang)

    generic_response = {
        "success": True,
        "message": backend_i18n.msg(lang, "auth.forgot_generic"),
    }

    if not is_valid_email(email):
        return generic_response

    user = vector_db.get_user_by_email(email)
    # Only verified accounts can log in, so only they may reset a password.
    if not user or not user.get("email_verified"):
        return generic_response

    reset_token = secrets.token_urlsafe(32)
    token_expires = (datetime.now() + timedelta(minutes=30)).isoformat()
    vector_db.set_password_reset_token(email, reset_token, token_expires)
    email_service.send_password_reset_email(
        email, reset_token, user.get("first_name", ""), lang
    )

    return generic_response

@app.post("/api/auth/reset-password")
def reset_password(request: ResetPasswordRequest):
    """Set a new password using the token from the password reset email."""
    token = request.token.strip()
    password = request.password
    confirm_password = request.confirm_password
    lang = backend_i18n.normalize_lang(request.lang)

    if len(password) < 4:
        raise HTTPException(status_code=400, detail=backend_i18n.msg(lang, "auth.password_short"))

    if password != confirm_password:
        raise HTTPException(status_code=400, detail=backend_i18n.msg(lang, "auth.password_mismatch"))

    user = vector_db.get_user_by_reset_token(token)
    if not user:
        raise HTTPException(
            status_code=400,
            detail=backend_i18n.msg(lang, "auth.reset_invalid_link"),
        )

    try:
        expires_at = datetime.fromisoformat(user.get("reset_token_expires") or "")
    except Exception:
        expires_at = None
    if expires_at and datetime.now() > expires_at:
        vector_db.clear_password_reset_token(user["id"])
        raise HTTPException(
            status_code=400,
            detail=backend_i18n.msg(lang, "auth.reset_expired"),
        )

    vector_db.update_user_password(user["id"], hash_password(password))
    # Any hijacked or stale sessions must die with the old password.
    vector_db.delete_user_sessions(user["id"])

    return {
        "success": True,
        "message": backend_i18n.msg(lang, "auth.reset_success"),
    }

def _verification_page(success: bool, message: str, login_url: str = None, lang: str = "en") -> HTMLResponse:
    """Render a simple server-side HTML page for the email verification link."""
    lang = backend_i18n.normalize_lang(lang)
    if success:
        icon = "✓"
        icon_bg = "#0d9488"
        action = (
            f'<a href="{login_url}" style="background:#0d9488;color:#fff;padding:12px 28px;border-radius:999px;text-decoration:none;font-weight:bold;font-size:14px;display:inline-block;">'
            f'{backend_i18n.msg(lang, "verify.go_to_login")}</a>'
            if login_url else ""
        )
    else:
        icon = "!"
        icon_bg = "#dc2626"
        action = (
            f'<p style="font-size:13px;color:#64748b;">{backend_i18n.msg(lang, "verify.resend_hint")}</p>'
        )

    heading = backend_i18n.msg(lang, "verify.success_heading" if success else "verify.failure_heading")
    page_title = backend_i18n.msg(lang, "verify.title")

    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{page_title}</title>
  <style>
    body {{ font-family: Arial, sans-serif; background: #f8fafc; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }}
    .card {{ background: #fff; border-radius: 16px; box-shadow: 0 10px 40px rgba(0,0,0,0.08); padding: 48px 40px; max-width: 440px; text-align: center; }}
    .icon {{ width: 64px; height: 64px; border-radius: 50%; background: {icon_bg}; color: #fff; font-size: 32px; font-weight: bold; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px; }}
    h1 {{ font-size: 22px; color: #0f172a; margin: 0 0 12px; }}
    p {{ font-size: 14px; color: #475569; line-height: 1.6; margin: 0 0 8px; }}
    .action {{ margin-top: 24px; }}
  </style>
</head>
<body>
  <div class="card">
    <div class="icon">{icon}</div>
    <h1>{heading}</h1>
    <p>{message}</p>
    <div class="action">{action}</div>
  </div>
</body>
</html>"""
    return HTMLResponse(content=html, status_code=200 if success else 400)

@app.post("/api/auth/logout")
def logout_user(current_user: dict = Depends(get_current_user), x_session_token: Optional[str] = Header(None), authorization: Optional[str] = Header(None)):
    token = x_session_token
    if not token and authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        
    if token:
        vector_db.delete_session(token)
    return {"success": True, "message": "Logged out successfully."}

@app.get("/api/auth/me")
def get_me(current_user: dict = Depends(get_current_user)):
    user_info = vector_db.get_user_by_id(current_user["user_id"])
    if not user_info:
        raise HTTPException(status_code=404, detail="User not found.")
    return {
        "email": user_info["email"],
        "chatbot_id": user_info["chatbot_id"],
        "has_custom_api_key": bool(user_info.get("api_key"))
    }

# Admin Settings Endpoints

@app.get("/api/settings")
def get_user_settings(current_user: dict = Depends(get_current_user)):
    """Retrieve user configurations and system defaults."""
    user_info = vector_db.get_user_by_id(current_user["user_id"])
    if not user_info:
        raise HTTPException(status_code=404, detail="User not found.")
    
    settings = user_info.get("settings", {})

    # Determine effective provider: user preference → global auto-detected default
    effective_provider = (settings.get("provider") or config.DEFAULT_PROVIDER or "gemini").lower()

    # Return the user's api_key for their active provider
    active_api_key = vector_db.get_user_provider_key(user_info, effective_provider) or user_info.get("api_key", "")

    return {
        "api_key": active_api_key,
        "settings": settings,
        "chatbot_id": current_user["chatbot_id"],
        "has_global_key": bool(config.get_api_key("gemini") or config.get_api_key("openai") or config.get_api_key("claude") or config.get_api_key("generic")),
        "global_keys_available": {
            "gemini": bool(config.get_api_key("gemini")),
            "openai": bool(config.get_api_key("openai")),
            "claude": bool(config.get_api_key("claude")),
            "generic": bool(config.get_api_key("generic")),
            "groq": bool(config.get_api_key("groq")),
            "openrouter": bool(config.get_api_key("openrouter")),
        },
        "default_provider": effective_provider,
        "default_models": config.DEFAULT_MODELS,
        "supported_providers": config.get_available_providers()
    }

@app.post("/api/settings")
def save_user_settings(request: SettingsRequest, current_user: dict = Depends(get_current_user)):
    """Save multi-provider API keys and configurations."""
    try:
        settings_payload = {}
        if request.provider:
            settings_payload["provider"] = request.provider.lower()
        if request.api_key is not None:
            settings_payload["api_key"] = request.api_key.strip()
        if request.gemini_key is not None:
            settings_payload["gemini_key"] = request.gemini_key.strip()
        if request.openai_key is not None:
            settings_payload["openai_key"] = request.openai_key.strip()
        if request.claude_key is not None:
            settings_payload["claude_key"] = request.claude_key.strip()
        if request.generic_key is not None:
            settings_payload["generic_key"] = request.generic_key.strip()
        if request.generic_base_url is not None:
            settings_payload["generic_base_url"] = request.generic_base_url.strip()
        if request.generic_model is not None:
            settings_payload["generic_model"] = request.generic_model.strip()

        vector_db.update_user_settings(current_user["user_id"], settings_payload)
        return {"success": True, "message": "Settings saved successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Indexing & Documents Endpoints

@app.get("/api/stats")
def get_stats(current_user: dict = Depends(get_current_user)):
    """Retrieve indexing statistics for the authenticated user's chatbot."""
    try:
        chatbot_id = current_user["chatbot_id"]
        stats = vector_db.get_stats(chatbot_id=chatbot_id)
        
        # Calculate size of documents belonging to this chatbot
        docs = vector_db.get_documents(chatbot_id=chatbot_id)
        uploads_size = sum(doc["file_size"] for doc in docs)
        stats["uploads_size_bytes"] = uploads_size
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/documents")
def list_documents(current_user: dict = Depends(get_current_user)):
    """Get all documents currently indexed for the authenticated user's chatbot."""
    try:
        chatbot_id = current_user["chatbot_id"]
        docs = vector_db.get_documents(chatbot_id=chatbot_id)
        # Check if analysis report exists for each document
        for doc in docs:
            analysis_path = os.path.join(config.DATA_DIR, f"analysis_{doc['id']}.md")
            doc["has_analysis"] = os.path.exists(analysis_path)
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload")
async def upload_document(
    file: UploadFile = File(...),
    api_key: Optional[str] = Form(None),
    provider: Optional[str] = Form(None),
    model: Optional[str] = Form(None),
    base_url: Optional[str] = Form(None),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload a document, extract text, chunk it, generate embeddings,
    and save raw content + vector references.
    """
    # Validation checks
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".pdf", ".txt", ".md", ".docx"]:
        raise HTTPException(status_code=400, detail="Only PDF, TXT, Markdown, and DOCX files are supported.")

    doc_id = str(uuid.uuid4())
    filename = file.filename
    temp_file_path = os.path.join(config.UPLOAD_DIR, f"{doc_id}{ext}")
    chatbot_id = current_user["chatbot_id"]
    
    # Resolve Provider and API Key — always prefer server .env config
    user_info = vector_db.get_user_by_id(current_user["user_id"])
    requested_provider = (
        config.DEFAULT_PROVIDER
        or "gemini"
    ).lower()

    resolved_api_key = (
        config.get_api_key(requested_provider)
        or (vector_db.get_user_provider_key(user_info, requested_provider) if user_info else None)
    )

    resolved_base_url = (
        config.get_base_url(requested_provider)
        or (user_info.get("settings", {}).get("generic_base_url") if user_info else None)
    )

    requested_model = (
        config.get_default_model(requested_provider)
    )

    try:
        # 1. Save uploaded file to disk
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        file_size = os.path.getsize(temp_file_path)

        # 2. Extract raw text
        raw_text = document_processor.extract_text_from_file(temp_file_path)
        if not raw_text.strip():
            raise ValueError("The uploaded document contains no readable text content.")

        # 3. Create document chunks
        chunks = document_processor.split_text_into_chunks(raw_text)
        chunk_count = len(chunks)
        if chunk_count == 0:
            raise ValueError("Failed to split text into logical sections.")

        # 4. Generate embeddings for chunks & build data list
        chunks_data = []
        for idx, chunk_text in enumerate(chunks):
            embedding = ai_agent.get_embedding(chunk_text, api_key=resolved_api_key, provider=requested_provider)
            chunks_data.append({
                "text": chunk_text,
                "embedding": embedding,
                "index": idx
            })

        # 5. Save document and chunks to SQLite
        vector_db.add_document(doc_id, filename, file_size, chunk_count, chatbot_id=chatbot_id)
        vector_db.add_chunks(doc_id, chunks_data)

        # 6. Generate background Analysis report
        analysis_report = ai_agent.analyze_full_document(
            filename=filename,
            full_text=raw_text,
            api_key=resolved_api_key,
            model_name=requested_model,
            provider=requested_provider,
            base_url=resolved_base_url
        )
        analysis_path = os.path.join(config.DATA_DIR, f"analysis_{doc_id}.md")
        with open(analysis_path, "w", encoding="utf-8") as f:
            f.write(analysis_report)


        return {
            "success": True,
            "document_id": doc_id,
            "filename": filename,
            "chunks_created": chunk_count,
            "has_analysis": True
        }

    except Exception as e:
        # Cleanup files on failure
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        
        # Diagnostics block to identify supported embedding models
        diagnostics = ""
        try:
            import google.generativeai as genai
            genai.configure(api_key=resolved_api_key)
            avail_models = []
            for m in genai.list_models():
                if 'embedContent' in m.supported_generation_methods:
                    avail_models.append(m.name)
            if avail_models:
                diagnostics = f" Supported embedding models: {', '.join(avail_models)}."
            else:
                diagnostics = " No embedding models reported as supported by this API key."
        except Exception as diag_err:
            diagnostics = f" (Diagnostics query failed: {str(diag_err)})"

        raise HTTPException(status_code=500, detail=f"Indexing failed: {str(e)}.{diagnostics}")

@app.delete("/api/documents/{doc_id}")
def delete_document(doc_id: str, current_user: dict = Depends(get_current_user)):
    """Remove document from filesystem, SQLite database, and delete its analysis report."""
    try:
        chatbot_id = current_user["chatbot_id"]
        # Retrieve document metadata first to get filename and check ownership
        docs = vector_db.get_documents(chatbot_id=chatbot_id)
        target_doc = next((d for d in docs if d["id"] == doc_id), None)
        
        if not target_doc:
            raise HTTPException(status_code=404, detail="Document not found or access denied.")

        # Delete database entries with ownership check
        vector_db.delete_document(doc_id, chatbot_id=chatbot_id)

        # Delete raw file from disk
        filename = target_doc["filename"]
        ext = os.path.splitext(filename)[1].lower()
        file_path = os.path.join(config.UPLOAD_DIR, f"{doc_id}{ext}")
        if os.path.exists(file_path):
            os.remove(file_path)

        # Delete analysis report
        analysis_path = os.path.join(config.DATA_DIR, f"analysis_{doc_id}.md")
        if os.path.exists(analysis_path):
            os.remove(analysis_path)

        return {"success": True, "message": f"Document '{filename}' deleted successfully."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/documents/{doc_id}/analysis")
def get_document_analysis(doc_id: str, current_user: dict = Depends(get_current_user)):
    """Fetch the generated markdown analysis report of the document."""
    chatbot_id = current_user["chatbot_id"]
    # Check ownership
    docs = vector_db.get_documents(chatbot_id=chatbot_id)
    target_doc = next((d for d in docs if d["id"] == doc_id), None)
    if not target_doc:
        raise HTTPException(status_code=404, detail="Document not found or access denied.")

    analysis_path = os.path.join(config.DATA_DIR, f"analysis_{doc_id}.md")
    if not os.path.exists(analysis_path):
        raise HTTPException(status_code=404, detail="Analysis report not found for this document.")
        
    try:
        with open(analysis_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"document_id": doc_id, "analysis_report": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================
# CHAT SESSION ENDPOINTS
# ============================================================

@app.post("/api/chat-sessions")
def create_chat_session(current_user: dict = Depends(get_current_user)):
    """Create a new chat session for the authenticated user."""
    session_id = "cs_" + str(uuid.uuid4())[:12]
    user_id = current_user["user_id"]
    chatbot_id = current_user["chatbot_id"]
    
    vector_db.create_chat_session(session_id, user_id, chatbot_id)
    session = vector_db.get_chat_session_by_id(session_id)
    
    return {
        "success": True,
        "session_id": session_id,
        "title": "New Chat",
        "session": session or {
            "id": session_id,
            "title": "New Chat",
            "user_id": user_id,
            "chatbot_id": chatbot_id,
            "question_count": 0
        }
    }

@app.get("/api/chat-sessions")
def list_chat_sessions(current_user: dict = Depends(get_current_user)):
    """Get all chat sessions for the authenticated user."""
    user_id = current_user["user_id"]
    chatbot_id = current_user["chatbot_id"]
    
    sessions = vector_db.get_chat_sessions(user_id, chatbot_id)
    return sessions

@app.get("/api/chat-sessions/{session_id}")
def get_chat_session(session_id: str, current_user: dict = Depends(get_current_user)):
    """Get a specific chat session with all its questions/messages."""
    session = vector_db.get_chat_session_by_id(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found.")
    
    # Verify ownership
    if session["user_id"] != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Access denied.")
    
    questions = vector_db.get_session_questions(session_id)
    
    return {
        "session": session,
        "questions": questions
    }

@app.delete("/api/chat-sessions/{session_id}")
def delete_chat_session(session_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a chat session and all its messages."""
    session = vector_db.get_chat_session_by_id(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found.")
    
    if session["user_id"] != current_user["user_id"] and session["chatbot_id"] != current_user["chatbot_id"]:
        raise HTTPException(status_code=403, detail="Access denied.")
    
    if session["chatbot_id"] == current_user["chatbot_id"]:
        vector_db.admin_delete_chat_session(session_id, session["chatbot_id"])
    else:
        vector_db.delete_chat_session(session_id, current_user["user_id"])
    return {"success": True, "message": "Chat session deleted."}


# ============================================================
# ENHANCED CHAT ENDPOINT (Session-Based)
# ============================================================

@app.post("/api/chat")
async def chat_with_agent(
    request: ChatRequest,
    x_api_key: Optional[str] = Header(None),
    authorization: Optional[str] = Header(None),
    x_session_token: Optional[str] = Header(None)
):
    """
    RAG Chat endpoint. Supports both document-based and general questions.
    Automatically classifies question type, stores in session, and generates response.
    """
    query = request.query
    history = [h.dict() for h in request.chat_history] if request.chat_history else []
    lang = backend_i18n.normalize_lang(request.lang)
    
    # 1. Validate chatbot_id
    chatbot_id = request.chatbot_id
    if not chatbot_id or not vector_db.validate_chatbot_id(chatbot_id):
        raise HTTPException(status_code=404, detail=backend_i18n.msg(lang, "widget.chatbot_not_found"))
        
    # 2. Resolve API key, provider, base_url, model
    user_info = vector_db.get_user_by_chatbot_id(chatbot_id)
    requested_provider = (
        request.provider
        or config.DEFAULT_PROVIDER
        or "gemini"
    ).lower()

    # Always prefer server .env keys — user-stored keys are just a fallback
    resolved_api_key = (
        config.get_api_key(requested_provider)
        or (vector_db.get_user_provider_key(user_info, requested_provider) if user_info else None)
    )

    resolved_base_url = (
        config.get_base_url(requested_provider)
        or (user_info.get("settings", {}).get("generic_base_url") if user_info else None)
    )

    requested_model = (
        request.model
        or config.get_default_model(requested_provider)
    )

    if not resolved_api_key and not (requested_provider in ("generic", "custom") and resolved_base_url):
        raise HTTPException(
            status_code=400,
            detail=backend_i18n.msg(lang, "chat.api_key_missing")
        )

    # 3. Resolve user_id from auth token
    user_id = None
    auth_token = x_session_token
    if not auth_token and authorization and authorization.startswith("Bearer "):
        auth_token = authorization.split(" ")[1]
    if auth_token:
        auth_session = vector_db.get_session(auth_token)
        if auth_session:
            user_id = auth_session["user_id"]

    should_save = request.save_session is not False

    # 4. Resolve or create chat session (only if saving session)
    chat_session_id = request.session_id if should_save else None
    if should_save and user_id:
        if chat_session_id:
            # Verify the session exists and belongs to the user
            cs = vector_db.get_chat_session_by_id(chat_session_id)
            if not cs or cs["user_id"] != user_id:
                chat_session_id = None
        
        if not chat_session_id:
            # Create new chat session
            chat_session_id = "cs_" + str(uuid.uuid4())[:12]
            vector_db.create_chat_session(chat_session_id, user_id, chatbot_id)

    try:
        # 5. Check if query is a simple greeting or pleasantry
        pleasantry = ai_agent.check_conversational_pleasantry(query, lang=lang)
        if pleasantry:
            question_type = "general"
        else:
            question_type = "document"

        # 6. Create question record (only if saving session)
        question_id = "q_" + str(uuid.uuid4())[:12]
        if should_save and user_id and chat_session_id:
            vector_db.add_question(
                question_id=question_id,
                session_id=chat_session_id,
                user_id=user_id,
                chatbot_id=chatbot_id,
                question=query,
                question_type=question_type,
                status="new"
            )

        answer = ""
        context = []
        source_info = ""

        if pleasantry:
            answer = pleasantry
            context = []
            source_info = ""
        else:
            # Check if any documents exist for this chatbot
            docs = vector_db.get_documents(chatbot_id=chatbot_id)
            if not docs:
                answer = backend_i18n.msg(lang, "chat.no_documents")
                context = []
                source_info = ""
            else:
                # Document-based RAG flow
                query_emb = ai_agent.get_embedding(query, api_key=resolved_api_key, provider=requested_provider)
                matches = vector_db.search_similar_chunks(query_emb, chatbot_id=chatbot_id, limit=4)

                max_score = max((m.get("score", 0.0) for m in matches), default=0.0)
                if not matches or max_score <= 0.0:
                    answer = backend_i18n.msg(lang, "chat.refusal")
                    context = []
                    source_info = ""
                else:
                    answer = ai_agent.generate_answer(
                        query=query,
                        context_chunks=matches,
                        api_key=resolved_api_key,
                        model_name=requested_model,
                        chat_history=history,
                        provider=requested_provider,
                        base_url=resolved_base_url,
                        lang=lang
                    )
                    # If answer indicates information wasn't found in documents, clear context citations
                    answer_lower = answer.lower()
                    if (
                        "couldn't find anything" in answer_lower
                        or "raise your query to administration" in answer_lower
                        or "cannot find this information" in answer_lower
                        or "kon niets vinden" in answer_lower
                        or "niets vinden voor je vraag" in answer_lower
                        or "voorleggen aan beheer" in answer_lower
                    ):
                        context = []
                        source_info = ""
                    else:
                        context = matches
                        source_info = ", ".join(set(m["filename"] for m in matches))

        # 8. Update question with AI response (only if saving session)
        if should_save and user_id and chat_session_id:
            vector_db.update_question_response(
                question_id=question_id,
                ai_response=answer,
                source=source_info,
                status="ai_answered"
            )

        # 9. Auto-generate session title from first question (only if saving session)
        if should_save and user_id and chat_session_id:
            cs = vector_db.get_chat_session_by_id(chat_session_id)
            if cs and cs["title"] == "New Chat":
                try:
                    title = ai_agent.generate_session_title(
                        query=query,
                        api_key=resolved_api_key,
                        model_name=requested_model,
                        provider=requested_provider,
                        base_url=resolved_base_url,
                        lang=lang
                    )
                    vector_db.update_chat_session_title(chat_session_id, title)
                except Exception:
                    pass

        return {
            "answer": answer,
            "context": context,
            "question_type": question_type,
            "question_id": question_id,
            "session_id": chat_session_id
        }

    except Exception as e:
        # Update question status to indicate failure (only if saving session)
        if should_save and user_id and chat_session_id:
            try:
                vector_db.update_question_response(
                    question_id=question_id,
                    ai_response=f"Error: {str(e)}",
                    status="needs_review"
                )
            except Exception:
                pass

        diagnostics = ""
        if requested_provider == "gemini":
            try:
                import google.generativeai as genai
                genai.configure(api_key=resolved_api_key)
                avail_models = []
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        avail_models.append(m.name)
                if avail_models:
                    diagnostics = f" Supported generation models: {', '.join(avail_models[:5])}."
            except Exception:
                pass

        raise HTTPException(status_code=500, detail=f"{str(e)}.{diagnostics}")


# ============================================================
# ADMIN DASHBOARD ENDPOINTS
# ============================================================

@app.get("/api/admin/analytics")
def get_admin_analytics(current_user: dict = Depends(get_current_user)):
    """Get dashboard analytics for the authenticated user's chatbot."""
    chatbot_id = current_user["chatbot_id"]
    analytics = vector_db.get_dashboard_analytics(chatbot_id)
    return analytics

@app.get("/api/admin/sessions")
def get_admin_sessions(
    search: str = Query("", description="Search term"),
    limit: int = Query(50, description="Max results"),
    offset: int = Query(0, description="Offset for pagination"),
    current_user: dict = Depends(get_current_user)
):
    """Get all chat sessions for admin dashboard."""
    chatbot_id = current_user["chatbot_id"]
    sessions = vector_db.get_all_chat_sessions(chatbot_id, search=search, limit=limit, offset=offset)
    return sessions

@app.get("/api/admin/sessions/{session_id}")
def get_admin_session_detail(session_id: str, current_user: dict = Depends(get_current_user)):
    """Get detailed view of a chat session with all its questions for admin."""
    session = vector_db.get_chat_session_by_id(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found.")
    
    if session["chatbot_id"] != current_user["chatbot_id"]:
        raise HTTPException(status_code=403, detail="Access denied.")
    
    questions = vector_db.get_session_questions(session_id)
    
    # Get user email
    user_info = vector_db.get_user_by_id(session["user_id"])
    
    return {
        "session": session,
        "questions": questions,
        "user_email": user_info["email"] if user_info else "Unknown"
    }

@app.get("/api/admin/questions")
def get_admin_questions(
    search: str = Query("", description="Search term"),
    status: str = Query("", description="Filter by status"),
    question_type: str = Query("", description="Filter by type"),
    limit: int = Query(50, description="Max results"),
    offset: int = Query(0, description="Offset for pagination"),
    current_user: dict = Depends(get_current_user)
):
    """Get all questions for admin dashboard with filtering."""
    chatbot_id = current_user["chatbot_id"]
    questions = vector_db.get_all_questions(
        chatbot_id,
        search=search,
        status_filter=status,
        question_type_filter=question_type,
        limit=limit,
        offset=offset
    )
    return questions

@app.get("/api/admin/questions/{question_id}")
def get_admin_question_detail(question_id: str, current_user: dict = Depends(get_current_user)):
    """Get detailed view of a single question for admin."""
    question = vector_db.get_question_by_id(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found.")
    
    if question["chatbot_id"] != current_user["chatbot_id"]:
        raise HTTPException(status_code=403, detail="Access denied.")
    
    return question

@app.put("/api/admin/questions/{question_id}")
def update_admin_question(question_id: str, update: AdminQuestionUpdate, current_user: dict = Depends(get_current_user)):
    """Admin: Update question status and/or provide admin response."""
    chatbot_id = current_user["chatbot_id"]
    
    # Validate status if provided
    valid_statuses = ["new", "ai_answered", "needs_review", "admin_answered", "resolved"]
    if update.status and update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
    
    try:
        vector_db.admin_update_question(
            question_id=question_id,
            chatbot_id=chatbot_id,
            status=update.status,
            admin_response=update.admin_response
        )
        return {"success": True, "message": "Question updated successfully."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/sessions/{session_id}")
def delete_admin_session(session_id: str, current_user: dict = Depends(get_current_user)):
    """Admin: Delete a chat session and all its messages."""
    chatbot_id = current_user["chatbot_id"]
    session = vector_db.get_chat_session_by_id(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found.")
    
    if session["chatbot_id"] != chatbot_id:
        raise HTTPException(status_code=403, detail="Access denied.")
    
    try:
        vector_db.admin_delete_chat_session(session_id, chatbot_id)
        return {"success": True, "message": "Chat session deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/questions/{question_id}")
def delete_admin_question(question_id: str, current_user: dict = Depends(get_current_user)):
    """Admin: Delete a query/question."""
    chatbot_id = current_user["chatbot_id"]
    try:
        vector_db.admin_delete_question(question_id, chatbot_id)
        return {"success": True, "message": "Query deleted successfully."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/widget/inquiry")
def submit_widget_inquiry(request: WidgetInquiryRequest):
    """
    Submit an escalation/inquiry directly from the chat widget to the Admin Dashboard.
    Captures email, title, and description from website users when policy info is insufficient.
    """
    chatbot_id = request.chatbot_id
    lang = backend_i18n.normalize_lang(request.lang)
    if not chatbot_id or not vector_db.validate_chatbot_id(chatbot_id):
        raise HTTPException(status_code=404, detail=backend_i18n.msg(lang, "widget.chatbot_not_found"))

    email = request.email.strip()
    if not email or not is_valid_email(email):
        raise HTTPException(status_code=400, detail=backend_i18n.msg(lang, "auth.invalid_email"))

    title = request.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail=backend_i18n.msg(lang, "widget.title_required"))

    description = request.description.strip()
    if not description:
        raise HTTPException(status_code=400, detail=backend_i18n.msg(lang, "widget.description_required"))

    try:
        result = vector_db.add_widget_inquiry(
            chatbot_id=chatbot_id,
            email=email,
            title=title,
            description=description
        )
        return {
            "success": True,
            "message": "Inquiry submitted successfully to HR Administration.",
            "question_id": result["question_id"],
            "session_id": result["session_id"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=backend_i18n.msg(lang, "widget.submit_failed", error=str(e))
        )

# ============================================================
# Serve Frontend & Static Assets
# ============================================================

FRONTEND_DIST_DIR = os.path.join(config.BASE_DIR, "frontend", "dist")

@app.get("/")
def read_index():
    """Serve the root dashboard application from the Vue 3 + Vite build."""
    vue_index = os.path.join(FRONTEND_DIST_DIR, "index.html")
    if os.path.exists(vue_index):
        return FileResponse(vue_index)
    return JSONResponse(
        status_code=404,
        content={"detail": "Frontend build not found. Please run 'npm run build' in the frontend directory."}
    )

@app.middleware("http")
async def serve_widget_script_fresh(request: Request, call_next):
    """Force embeddable widget scripts to always revalidate so stale browser caches never hide new features."""
    response = await call_next(request)
    if request.url.path.endswith("widget.js"):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response

WIDGET_SCRIPT_CANDIDATES = [
    os.path.join(config.STATIC_DIR, "widget.js"),
    os.path.join(FRONTEND_DIST_DIR, "widget.js"),
]

def _latest_widget_path() -> str:
    available = [path for path in WIDGET_SCRIPT_CANDIDATES if os.path.exists(path)]
    if not available:
        raise HTTPException(status_code=404, detail="widget.js not found")
    return max(available, key=os.path.getmtime)

@app.get("/widget.js")
def read_widget():
    """Serve the standalone embeddable widget script, always the freshest copy available."""
    return FileResponse(_latest_widget_path(), media_type="application/javascript")

# Mount assets directory for Vue Vite build
if os.path.exists(os.path.join(FRONTEND_DIST_DIR, "assets")):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST_DIR, "assets")), name="assets")

# Mount static folder for widget and other public assets
app.mount("/static", StaticFiles(directory=config.STATIC_DIR), name="static")
