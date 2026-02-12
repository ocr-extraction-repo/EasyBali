from motor.motor_asyncio import AsyncIOMotorClient
from app.settings.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client.get_database('easybali-db')
order_collection = db["orders-summary"]
villa_code_collection = db['villa-codes']