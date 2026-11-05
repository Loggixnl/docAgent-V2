import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _resolve_data_dir():
    # 1. Custom DATA_DIR environment variable
    explicit = os.getenv("DATA_DIR", "").strip()
    if explicit:
        return os.path.abspath(explicit)
    # 2. Check persistent volume mount points (Railway, Render, Fly.io, Docker)
    for candidate in ["/app/data", "/data"]:
        try:
            if os.path.exists(candidate) and os.path.isdir(candidate) and os.access(candidate, os.W_OK):
                return candidate
        except Exception:
            pass
    # 3. Default to local data directory
    return os.path.join(BASE_DIR, "data")

DATA_DIR = _resolve_data_dir()
UPLOAD_DIR = os.getenv("UPLOAD_DIR", os.path.join(DATA_DIR, "uploads"))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Database configuration: PostgreSQL via DATABASE_URL or SQLite via DB_PATH
DATABASE_URL = (
    os.getenv("DATABASE_URL", "").strip()
    or os.getenv("POSTGRES_URL", "").strip()
    or os.getenv("POSTGRESQL_URL", "").strip()
    or None
)
DB_PATH = os.getenv("DB_PATH", os.path.join(DATA_DIR, "vector_store.db"))

# App base URL (backend origin — used for API callbacks that must stay on the backend)
APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:8000").strip().rstrip("/")
# Frontend URL used to build verification email links:
#   <FRONTEND>/api/auth/verify-email?token=...&lang=...
# Falls back to the production frontend when APP_BASE_URL is the known
# production backend but APP_FRONTEND_URL is unset; otherwise to APP_BASE_URL.
_PRODUCTION_BACKEND_URL = "https://docagent-v2-production.up.railway.app"
_PRODUCTION_FRONTEND_URL = "https://docagent-v2-frontend-production.up.railway.app"
APP_FRONTEND_URL = (
    os.getenv("APP_FRONTEND_URL", "").strip().rstrip("/")
    or (_PRODUCTION_FRONTEND_URL if APP_BASE_URL == _PRODUCTION_BACKEND_URL else APP_BASE_URL)
)

# SMTP configuration for outgoing email (verification, etc.)
SMTP_HOST = os.getenv("SMTP_HOST", "").strip()
SMTP_PORT = int(os.getenv("SMTP_PORT", "587") or 587)
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "").strip()
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "").strip()
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", "").strip() or SMTP_USERNAME
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "DocAgent AI").strip()
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").strip().lower() not in ("false", "0", "no")
SMTP_USE_SSL = os.getenv("SMTP_USE_SSL", "false").strip().lower() in ("true", "1", "yes")

# SendGrid configuration for outgoing email (verification, etc.)
# Takes precedence over SMTP when SENDGRID_API_KEY and SENDGRID_TEMPLATE_ID are set.
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "").strip()
SENDGRID_TEMPLATE_ID = os.getenv("SENDGRID_TEMPLATE_ID", "").strip()
SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL", "noreply@docagent.ai").strip()
SENDGRID_FROM_NAME = os.getenv("SENDGRID_FROM_NAME", SMTP_FROM_NAME).strip()
SENDGRID_SUBJECT = os.getenv("SENDGRID_SUBJECT", "Account validation").strip()
# Dutch (nl) dynamic template. When empty, nl falls back to SENDGRID_TEMPLATE_ID.
SENDGRID_TEMPLATE_ID_NL = os.getenv("SENDGRID_TEMPLATE_ID_NL", "").strip()
SENDGRID_SUBJECT_NL = os.getenv("SENDGRID_SUBJECT_NL", "Account validering").strip()

# Supported UI languages (en = English, nl = Dutch)
SUPPORTED_LANGS = ("en", "nl")
DEFAULT_LANG = "en"

def normalize_lang(lang) -> str:
    """Return a supported language code, falling back to the default."""
    try:
        code = (lang or "").strip().lower()
    except Exception:
        code = ""
    return code if code in SUPPORTED_LANGS else DEFAULT_LANG

# CORS configuration
# Explicit allowed origins (comma-separated). Defaults cover the production
# frontend and local dev servers. Override with the CORS_ORIGINS env var.
_CORS_DEFAULT_ORIGINS = ",".join([
    "https://docagent-v2-frontend-production.up.railway.app",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
])
_cors_origins_raw = os.getenv("CORS_ORIGINS", "").strip() or _CORS_DEFAULT_ORIGINS
CORS_ORIGINS = [o.strip() for o in _cors_origins_raw.split(",") if o.strip()]

# Regex of origins allowed on top of the list. Defaults to any Railway app
# domain (Railway regenerates subdomains on redeploy). Set to "off" to disable.
_cors_regex_raw = os.getenv("CORS_ORIGIN_REGEX", "").strip()
if _cors_regex_raw.lower() in ("off", "false", "none", "disabled"):
    CORS_ORIGIN_REGEX = None
else:
    CORS_ORIGIN_REGEX = _cors_regex_raw or r"https://[a-z0-9-]+\.up\.railway\.app"

# Set to true to allow ANY origin (disables credentials). Use only for debugging.
CORS_ALLOW_ALL = os.getenv("CORS_ALLOW_ALL", "").strip().lower() in ("true", "1", "yes")

# Provider Configuration
# Supported providers: "gemini", "openai", "claude", "generic", "openrouter", "groq"
def _detect_default_provider():
    """Auto-detect provider from available API keys when DEFAULT_PROVIDER is not set explicitly."""
    explicit = os.getenv("DEFAULT_PROVIDER", "").strip().lower()
    if explicit:
        return explicit
    # Fall back to whichever key is actually present
    if os.getenv("GEMINI_API_KEY", ""):
        return "gemini"
    if os.getenv("OPENAI_API_KEY", ""):
        return "openai"
    if os.getenv("ANTHROPIC_API_KEY", "") or os.getenv("CLAUDE_API_KEY", ""):
        return "claude"
    if os.getenv("GROQ_API_KEY", ""):
        return "groq"
    if os.getenv("OPENROUTER_API_KEY", ""):
        return "openrouter"
    if os.getenv("GENERIC_API_KEY", ""):
        return "generic"
    return "gemini"  # final fallback

DEFAULT_PROVIDER = _detect_default_provider()

# API Keys - load from environment (set these in .env or pass explicitly)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY", "") or os.getenv("CLAUDE_API_KEY", "")
ANTHROPIC_API_KEY = CLAUDE_API_KEY
GENERIC_API_KEY = (
    os.getenv("GENERIC_API_KEY", "")
    or os.getenv("CUSTOM_API_KEY", "")
    or os.getenv("GROQ_API_KEY", "")
    or os.getenv("OPENROUTER_API_KEY", "")
)

# Custom Base URLs for OpenAI-compatible generic endpoints
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "").strip() or None
GENERIC_BASE_URL = (
    os.getenv("GENERIC_BASE_URL", "").strip()
    or os.getenv("CUSTOM_BASE_URL", "").strip()
    or (os.getenv("GROQ_API_KEY") and "https://api.groq.com/openai/v1")
    or (os.getenv("OPENROUTER_API_KEY") and "https://openrouter.ai/api/v1")
    or None
)

# Default Models per provider
DEFAULT_MODELS = {
    "gemini": os.getenv("GEMINI_MODEL", "models/gemini-2.0-flash"),
    "openai": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    "claude": os.getenv("CLAUDE_MODEL", "claude-3-5-haiku-20241022"),
    "anthropic": os.getenv("CLAUDE_MODEL", "claude-3-5-haiku-20241022"),
    "generic": os.getenv("GENERIC_MODEL", "llama-3.3-70b-versatile"),
    "custom": os.getenv("GENERIC_MODEL", "llama-3.3-70b-versatile"),
    "groq": os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
    "openrouter": os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct"),
}

DEFAULT_LLM_MODEL = DEFAULT_MODELS.get(DEFAULT_PROVIDER, "models/gemini-2.0-flash")
DEFAULT_EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "models/gemini-embedding-001")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

# Ensure required directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

def get_api_key(provider=None):
    """Retrieve API key for the given provider, or default provider from environment."""
    prov = (provider or DEFAULT_PROVIDER or "gemini").lower()
    if prov == "gemini":
        return os.getenv("GEMINI_API_KEY", "")
    elif prov == "openai":
        return os.getenv("OPENAI_API_KEY", "")
    elif prov in ("claude", "anthropic"):
        return os.getenv("ANTHROPIC_API_KEY", "") or os.getenv("CLAUDE_API_KEY", "")
    elif prov in ("generic", "custom"):
        return (
            os.getenv("GENERIC_API_KEY", "")
            or os.getenv("CUSTOM_API_KEY", "")
            or os.getenv("GROQ_API_KEY", "")
            or os.getenv("OPENROUTER_API_KEY", "")
            or os.getenv("OPENAI_API_KEY", "")
        )
    elif prov == "groq":
        return os.getenv("GROQ_API_KEY", "") or os.getenv("GENERIC_API_KEY", "")
    elif prov == "openrouter":
        return os.getenv("OPENROUTER_API_KEY", "") or os.getenv("GENERIC_API_KEY", "")
    return os.getenv("GEMINI_API_KEY", "")

def get_base_url(provider=None):
    """Retrieve base URL for OpenAI-compatible providers (Generic, Ollama, Groq, OpenRouter)."""
    prov = (provider or DEFAULT_PROVIDER or "gemini").lower()
    if prov == "openai":
        return os.getenv("OPENAI_BASE_URL", "").strip() or None
    elif prov in ("generic", "custom"):
        return (
            os.getenv("GENERIC_BASE_URL", "").strip()
            or os.getenv("CUSTOM_BASE_URL", "").strip()
            or None
        )
    elif prov == "groq":
        return os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1").strip()
    elif prov == "openrouter":
        return os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1").strip()
    return None

def get_default_model(provider=None):
    """Retrieve default model identifier for the provider."""
    prov = (provider or DEFAULT_PROVIDER or "gemini").lower()
    return DEFAULT_MODELS.get(prov, "models/gemini-2.0-flash")

def get_available_providers():
    """List of all supported LLM providers."""
    return ["gemini", "openai", "claude", "generic", "groq", "openrouter"]

