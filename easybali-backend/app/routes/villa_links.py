import logging
import re
from urllib.parse import quote

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse

from app.services.menu_services import get_villa_data


logger = logging.getLogger(__name__)
router = APIRouter(tags=["villa_links"])
_VILLA_CODE_PATTERN = re.compile(r"^V\d+$", re.IGNORECASE)


def _format_villa_name(name: str) -> str:
    formatted = name.replace("_", " ").replace("-", " ")
    return " ".join(word.capitalize() for word in formatted.split())


def _normalize_villa_code(villa_code: str | None) -> str | None:
    if not villa_code:
        return None
    normalized = villa_code.strip().upper()
    if not _VILLA_CODE_PATTERN.match(normalized):
        return None
    return normalized


async def _resolve_villa_code_by_name(villa_name: str) -> str | None:
    try:
        villas_df = await get_villa_data()
        if villas_df is None or villas_df.empty:
            return None

        exact_match = villas_df[villas_df["Name of Villa"].str.lower() == villa_name.lower()]
        if exact_match.empty:
            exact_match = villas_df[villas_df["Name of Villa"].str.contains(villa_name, case=False, na=False)]
        if exact_match.empty:
            return None

        code = str(exact_match.iloc[0]["Number"]).strip().upper()
        return code if _VILLA_CODE_PATTERN.match(code) else None
    except Exception as exc:
        logger.warning(f"Unable to resolve villa code for '{villa_name}': {exc}")
        return None


@router.get("/villa/{villa_name}")
async def villa_redirect(villa_name: str, code: str | None = Query(default=None)):
    try:
        formatted_villa_name = _format_villa_name(villa_name)
        resolved_code = _normalize_villa_code(code)
        if not resolved_code:
            resolved_code = await _resolve_villa_code_by_name(formatted_villa_name)

        bot_number = "6282247959788"
        welcome_text = f"Hi, I am in {formatted_villa_name}"
        if resolved_code:
            welcome_text = f"{welcome_text} [VILLA_CODE:{resolved_code}]"

        whatsapp_url = f"https://wa.me/{bot_number}?text={quote(welcome_text)}"
        return RedirectResponse(url=whatsapp_url)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception(f"Error in villa redirect: {exc}")
        raise HTTPException(status_code=500, detail="Service temporarily unavailable")
