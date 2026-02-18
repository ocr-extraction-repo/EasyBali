import uvicorn
import os
import logging
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Normalize common Render env-var pasting issues (surrounding quotes, literal \n sequences).
def _strip_outer_quotes(value: str) -> str:
    if not isinstance(value, str):
        return value
    s = value.strip()
    if len(s) >= 2 and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
        return s[1:-1]
    return s


def _normalize_pem_multiline(value: str) -> str:
    """Convert literal \\n sequences into real newlines for PEM blocks."""
    if not isinstance(value, str):
        return value
    s = _strip_outer_quotes(value)
    if "\\n" in s and "\n" not in s:
        s = s.replace("\\n", "\n")
    return s


def _normalize_google_creds_json(value: str) -> str:
    """Ensure service account JSON is a JSON object string; normalize private_key newlines."""
    if not isinstance(value, str) or not value.strip():
        return value

    raw = _strip_outer_quotes(value)
    try:
        parsed = json.loads(raw)
        # Handle accidentally double-encoded JSON (string containing JSON).
        if isinstance(parsed, str):
            parsed = json.loads(parsed)
        if isinstance(parsed, dict):
            pk = parsed.get("private_key")
            if isinstance(pk, str) and "\\n" in pk and "\n" not in pk:
                parsed["private_key"] = pk.replace("\\n", "\n")
            return json.dumps(parsed)
    except Exception:
        return raw

    return raw

# ─────────────────────────────────────────────────
# Pre-startup: Write credential files from env vars
# (Render doesn't have the files, so we inject via env)
# ─────────────────────────────────────────────────
def _write_credential_files():
    """Write credential files from environment variables if they don't exist on disk."""
    # Google Sheets credentials
    google_creds = _normalize_google_creds_json(os.environ.get("GOOGLE_CREDENTIALS_JSON"))
    creds_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "easy-bali-b74b61110525.json")
    if google_creds and not os.path.exists(creds_path):
        try:
            with open(creds_path, "w") as f:
                f.write(google_creds)
            logger.info("Google credentials written from env var")
        except Exception as e:
            logger.warning(f"Could not write Google credentials: {e}")
    # WhatsApp private key
    pem_content = _normalize_pem_multiline(os.environ.get("WHATSAPP_PRIVATE_KEY_PEM"))
    pem_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "private.pem")
    if pem_content and not os.path.exists(pem_path):
        try:
            with open(pem_path, "w") as f:
                f.write(pem_content)
            logger.info("Private key written from env var")
        except Exception as e:
            logger.warning(f"Could not write private key: {e}")
_write_credential_files()
# ─────────────────────────────────────────────────
# Import routers
# ─────────────────────────────────────────────────
from app.routes.main_menu_routes import router as menu_router
from app.routes.chatbot_routes import router as chat_router
from app.routes.whatsapp_routes import router as whatsapp_router
from app.routes.things_to_do_in_Bali import router as things_bali
from app.routes.event_calender import router as event_calender
from app.routes.local_cuisine import router as local_cuisine
from app.routes.what_to_do import router as what_to_do
from app.routes.plan_my_trip import router as plan_my_trip
from app.routes.language_lesson import router as language_lesson
from app.routes.websockett import router as web_order_flow
from app.routes.currency_route import router as currency_converter
from app.routes.villa_links import router as villa_links_router
from app.routes.payment_recovery_routes import router as payment_recovery_router
from app.services.menu_services import start_cache_refresh, stop_cache_refresh
# ─────────────────────────────────────────────────
# FastAPI App
# ─────────────────────────────────────────────────
app = FastAPI(
    title="Easy-Bali Chatbot",
    description="API's for easy-bali chatbot",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include routes
app.include_router(menu_router)
app.include_router(chat_router)
app.include_router(whatsapp_router)
app.include_router(things_bali)
app.include_router(event_calender)
app.include_router(local_cuisine)
app.include_router(what_to_do)
app.include_router(plan_my_trip)
app.include_router(web_order_flow)
app.include_router(language_lesson)
app.include_router(currency_converter)
app.include_router(villa_links_router)
app.include_router(payment_recovery_router, tags=["Payment Recovery"])

@app.on_event("startup")
def on_startup():
    try:
        start_cache_refresh()
        logger.info("Cache refresh started")
    except Exception as e:
        logger.warning(f"Cache refresh failed to start: {e}")

@app.on_event("shutdown")
def on_shutdown():
    try:
        stop_cache_refresh()
    except Exception:
        pass

@app.on_event("startup")
async def init():
    """Verify OpenAI connectivity (non-fatal if fails)."""
    try:
        from app.services.openai_client import client
        await client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "System check"}]
        )
        logger.info("OpenAI connection verified")
    except Exception as e:
        logger.warning(f"OpenAI init check failed (non-fatal): {e}")

@app.get("/")
def read_root():
    return {"msg": "Welcome to EASY-BALI chatbot", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "easybali-backend"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
