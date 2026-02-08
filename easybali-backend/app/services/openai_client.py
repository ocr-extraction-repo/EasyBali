from app.settings.config import settings
from openai import AsyncOpenAI


client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)