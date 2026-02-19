from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import Optional
import logging
import os
from pydantic import field_validator
from urllib.parse import quote, unquote

load_dotenv()

logger = logging.getLogger(__name__)


def _strip_outer_quotes(value: str) -> str:
    s = value.strip()
    if len(s) >= 2 and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
        return s[1:-1]
    return s


def _normalize_mongo_uri(value: str) -> str:
    """
    Normalize MongoDB URI credentials so common paste issues don't break auth.
    Example fixed: mongodb+srv://user:pass@word@cluster...
    """
    if not isinstance(value, str) or not value.strip():
        return value

    raw = _strip_outer_quotes(value.strip())
    if not raw.startswith(("mongodb://", "mongodb+srv://")):
        return raw

    scheme, sep, remainder = raw.partition("://")
    if not sep or not remainder:
        return raw

    # Split on the LAST @ to isolate host portion even if password contains @.
    auth_part, at, host_part = remainder.rpartition("@")
    if not at or not auth_part or not host_part:
        return raw

    username, colon, password = auth_part.partition(":")
    if not colon:
        return raw

    safe_username = quote(unquote(username), safe="-._~")
    safe_password = quote(unquote(password), safe="-._~")
    return f"{scheme}://{safe_username}:{safe_password}@{host_part}"


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

    @field_validator("MONGO_URI", mode="after")
    @classmethod
    def _normalize_mongo_uri_value(cls, v):
        return _normalize_mongo_uri(v)

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
