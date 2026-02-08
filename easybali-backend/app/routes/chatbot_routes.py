from fastapi import APIRouter
from app.schemas.ai_response import ChatbotResponse
from app.models.chatbot_models import ChatRequest
from app.services.ai_prompt import generate_response

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

@router.post("/generate-response", response_model=ChatbotResponse)
async def generate_chatbot_response(request: ChatRequest, user_id: str):
    query = request.query
    return await generate_response(query, user_id)