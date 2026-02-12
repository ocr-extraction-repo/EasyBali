from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import Optional
import logging
import os

load_dotenv()

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    # All fields use Optional with defaults so the app can START
    # even if some env vars are missing (warns instead of crashing)
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL_NAME: str = "gpt-4o"
    whatsapp_api_url: str = ""
    access_token: str = ""
    verify_token: str = ""
    AWS_ACCESS_KEY: str = ""
    AWS_SECRET_KEY: str = ""
    AWS_BUCKET_NAME: str = ""
    AWS_REGION: str = ""
    MONGO_URI: str = ""
    pinecone_api_key: str = ""
    pinecone_region: str = ""
    pinecone_cloud: str = ""
    XENDIT_SECRET_KEY: str = ""
    BASE_URL: str = ""
    WEB_BASE_URL: str = ""
    WHATSAPP_APP_SECRET: str = ""
    WHATSAPP_PRIVATE_KEY_PASSWORD: str = ""

    # New: env-var based credential injection for Render
    GOOGLE_CREDENTIALS_JSON: str = ""
    WHATSAPP_PRIVATE_KEY_PEM: str = ""

    class Config:
        env_file = ".env"


settings = Settings()

# Warn about missing critical vars (non-fatal)
_critical = [
    "OPENAI_API_KEY", "MONGO_URI", "access_token",
    "whatsapp_api_url", "verify_token"
]
for var in _critical:
    if not getattr(settings, var, ""):
        logger.warning(f"⚠️  Missing env var: {var}")