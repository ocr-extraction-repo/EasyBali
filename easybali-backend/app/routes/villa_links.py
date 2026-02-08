import uuid
import re
from datetime import datetime, timedelta

from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from fastapi import APIRouter

temp_villa_sessions = {}

router = APIRouter(tags=["villa_links"])



# def is_valid_villa_code(villa_code: str):
#     pattern = r'^V\d+$'
#     return bool(re.match(pattern, villa_code.upper()))


@router.get("/villa/{villa_name}")
async def villa_redirect(villa_name: str):
    try:
        def format_villa_name(name: str) -> str:
            formatted = name.replace('_', ' ').replace('-', ' ')
            formatted = ' '.join(word.capitalize() for word in formatted.split())
            return formatted
        

        formatted_villa_name = format_villa_name(villa_name)

        bot_number = "6282247959788"

        welcome_text = f"Hi, I am in {formatted_villa_name}       "
        whatsapp_url = f"https://wa.me/{bot_number}?text={welcome_text}"
        
        return RedirectResponse(url=whatsapp_url)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in villa redirect: {e}")
        raise HTTPException(status_code=500, detail="Service temporarily unavailable")


# def get_villa_from_temp_session(session_id: str):
#     """Get villa code from temporary session"""
#     session_data = temp_villa_sessions.get(session_id)
    
#     if not session_data:
#         return None
    
#     # Check if session is expired (10 minutes)
#     if datetime.now() - session_data["timestamp"] > timedelta(minutes=10):
#         temp_villa_sessions.pop(session_id, None)
#         return None
    
#     return session_data["villa_code"]

# def cleanup_temp_session(session_id: str):
#     """Remove temporary session after use"""
#     temp_villa_sessions.pop(session_id, None)

# def cleanup_expired_sessions():
#     """Clean up expired sessions"""
#     current_time = datetime.now()
#     expired_sessions = [
#         session_id for session_id, data in temp_villa_sessions.items()
#         if current_time - data["timestamp"] > timedelta(minutes=10)
#     ]
    
#     for session_id in expired_sessions:
#         temp_villa_sessions.pop(session_id, None)