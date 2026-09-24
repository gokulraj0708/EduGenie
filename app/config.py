import os
from dotenv import load_dotenv

load_dotenv()

# API Keys - support both naming conventions
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
GOOGLE_API_KEY = GEMINI_API_KEY

# Model configuration
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
USE_LOCAL_MODEL = os.getenv("USE_LOCAL_MODEL", "false").lower() == "true"

# Server config
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

def has_gemini_key() -> bool:
    return bool(GEMINI_API_KEY and len(GEMINI_API_KEY.strip()) > 10)

def get_gemini_model_name() -> str:
    return GEMINI_MODEL
