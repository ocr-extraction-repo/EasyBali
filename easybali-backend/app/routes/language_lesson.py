from fastapi import APIRouter, HTTPException
from fastapi import HTTPException
from app.schemas.ai_response import ChatbotQuery
from app.services.language import optimizer



router = APIRouter(prefix="/language_lesson", tags=["Chatbot"])

@router.post("/chat")
async def ultra_chat_endpoint(request: ChatbotQuery, user_id:str):
    try:
        sanitized_input = request.query.strip().replace('\n', ' ')
        if not sanitized_input:
            raise HTTPException(status_code=400, detail="Empty message received")
        
        response = await optimizer.quantum_response(user_id, sanitized_input)
        
        return {"response": response,}
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {e}")
