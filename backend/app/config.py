# app/config.py
import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv
from datetime import timedelta

ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT / ".env"
load_dotenv(ENV_FILE, override=False) 
SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret")
ALGORITHM = "HS256"
#ACCESS_TOKEN_EXPIRE_MINUTES = 60

class Settings(BaseModel):
    # ML Model settings
    USE_ML_MODEL: bool = os.getenv("USE_ML_MODEL", "true").strip().lower() == "true"
    ML_MODEL_PATH: Optional[str] = os.getenv("ML_MODEL_PATH")  # Optional custom path
    ML_VECTORIZER_PATH: Optional[str] = os.getenv("ML_VECTORIZER_PATH")  # Optional custom path
    
    # OpenAI settings (fallback)
    USE_OPENAI: bool = os.getenv("USE_OPENAI", "false").strip().lower() == "true"
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4.1-nano")

    RB_MIN_CONF: float = float(os.getenv("RB_MIN_CONF", "0.70"))
    MAX_BODY_CHARS: int = int(os.getenv("MAX_BODY_CHARS", "8000"))

settings = Settings()
