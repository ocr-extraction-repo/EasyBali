import logging
import re
from io import BytesIO
from urllib.parse import quote

import qrcode
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response

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


async def _resolve_code(villa_name: str, code: str | None) -> str | None:
    resolved_code = _normalize_villa_code(code)
    if resolved_code:
        return resolved_code
    return await _resolve_villa_code_by_name(_format_villa_name(villa_name))


def _build_landing_url(request: Request, villa_name: str, resolved_code: str | None) -> str:
    landing_url = str(request.url_for("villa_redirect", villa_name=villa_name))
    if resolved_code:
        landing_url = f"{landing_url}?code={resolved_code}"
    return landing_url


@router.get("/villa/{villa_name}/qr.png")
async def villa_qr_png(
    request: Request,
    villa_name: str,
    code: str | None = Query(default=None),
    box_size: int = Query(default=12, ge=2, le=30),
):
    resolved_code = await _resolve_code(villa_name, code)
    landing_url = _build_landing_url(request, villa_name, resolved_code)

    qr = qrcode.QRCode(version=1, box_size=box_size, border=4)
    qr.add_data(landing_url)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    qr_image.save(buffer, format="PNG")
    return Response(content=buffer.getvalue(), media_type="image/png")


@router.get("/villa/{villa_name}/qr", response_class=HTMLResponse)
async def villa_qr_page(request: Request, villa_name: str, code: str | None = Query(default=None)):
    resolved_code = await _resolve_code(villa_name, code)
    landing_url = _build_landing_url(request, villa_name, resolved_code)
    qr_png_url = str(request.url_for("villa_qr_png", villa_name=villa_name))
    if resolved_code:
        qr_png_url = f"{qr_png_url}?code={resolved_code}"

    code_line = resolved_code if resolved_code else "No code resolved"
    html = f"""<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Villa QR</title>
    <style>
      body {{ font-family: Arial, sans-serif; padding: 24px; text-align: center; }}
      img {{ max-width: min(90vw, 420px); border: 1px solid #ddd; border-radius: 8px; }}
      .meta {{ margin-top: 14px; font-size: 14px; word-break: break-all; }}
      .code {{ font-weight: bold; }}
    </style>
  </head>
  <body>
    <h2>EASY Bali Villa QR</h2>
    <p class="code">Code: {code_line}</p>
    <img src="{qr_png_url}" alt="Villa QR Code" />
    <p class="meta">Scan this QR with phone camera.</p>
    <p class="meta">Target URL: {landing_url}</p>
  </body>
</html>"""
    return HTMLResponse(content=html)


@router.get("/villa/{villa_name}")
async def villa_redirect(villa_name: str, code: str | None = Query(default=None)):
    try:
        formatted_villa_name = _format_villa_name(villa_name)
        resolved_code = await _resolve_code(villa_name, code)

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
