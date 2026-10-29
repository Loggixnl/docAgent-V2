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

