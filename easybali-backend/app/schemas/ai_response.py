from pydantic import BaseModel
from typing import Optional, List, Dict

class ChatbotResponse(BaseModel):
    response: str

class ChatbotQuery(BaseModel):
    query: str