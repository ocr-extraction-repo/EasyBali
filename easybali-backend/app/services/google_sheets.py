import gspread
import json
import os
import tempfile
import logging
from google.oauth2.service_account import Credentials

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDENTIALS_FILE = "easy-bali-b74b61110525.json"


def _get_credentials_path() -> str:
    """Resolve credentials: filesystem file → env var → error."""
    # 1. Check if file exists on disk (local dev)
    if os.path.exists(CREDENTIALS_FILE):
        return CREDENTIALS_FILE

    # 2. Check relative to app root
    app_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    alt_path = os.path.join(app_root, CREDENTIALS_FILE)
    if os.path.exists(alt_path):
        return alt_path

    # 3. Check env var (Render deployment)
    env_json = os.environ.get("GOOGLE_CREDENTIALS_JSON", "")
    if env_json:
        try:
            tmp_path = os.path.join(tempfile.gettempdir(), CREDENTIALS_FILE)
            with open(tmp_path, "w") as f:
                f.write(env_json)
            logger.info("✅ Google credentials loaded from env var")
            return tmp_path
        except Exception as e:
            logger.error(f"❌ Failed to write Google credentials from env: {e}")

    logger.warning("⚠️  Google credentials file not found")
    return CREDENTIALS_FILE  # Will fail at runtime if truly missing


def get_workbook(sheet_id: str):
    creds_path = _get_credentials_path()
    creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open_by_key(sheet_id)
