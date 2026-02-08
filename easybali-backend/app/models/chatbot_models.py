from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str

class MenuRequest(BaseModel):
    type: str

class ServiceRequest(BaseModel):
    serviceitem_type: str