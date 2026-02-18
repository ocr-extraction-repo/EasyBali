from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import Optional
import logging
import os
from pydantic import field_validator

load_dotenv()

logger = logging.getLogger(__name__)


def _strip_outer_quotes(value: str) -> str:
    s = value.strip()
    if len(s) >= 2 and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
        return s[1:-1]
    return s


class Settings(BaseSettings):
    APP_ENV: str = "development"
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
    XENDIT_WEBHOOK_CALLBACK_TOKEN: str = ""
    XENDIT_WEBHOOK_PATH: str = "/webhook/xendit"
    XENDIT_ENABLE_DISBURSEMENT: bool = False
    BASE_URL: str = ""
    WEB_BASE_URL: str = ""
    WHATSAPP_APP_SECRET: str = ""
    WHATSAPP_PRIVATE_KEY_PASSWORD: str = ""

    # New: env-var based credential injection for Render
    GOOGLE_CREDENTIALS_JSON: str = ""
    WHATSAPP_PRIVATE_KEY_PEM: str = ""

    # Render users sometimes paste values with surrounding quotes, e.g. MONGO_URI="mongodb+srv://..."
    # Strip only ONE outer quote pair so URIs/keys parse correctly.
    @field_validator("*", mode="before")
    @classmethod
    def _normalize_env_strings(cls, v):
        if isinstance(v, str) and v:
            return _strip_outer_quotes(v)
        return v

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
        logger.warning(f"Missing env var: {var}")
if settings.APP_ENV.lower() == "production" and not settings.XENDIT_ENABLE_DISBURSEMENT:
    logger.warning("XENDIT_ENABLE_DISBURSEMENT is disabled in production.")
