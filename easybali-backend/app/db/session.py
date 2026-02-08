from motor.motor_asyncio import AsyncIOMotorClient
from app.settings.config import settings

client = AsyncIOMotorClient(settings.MONGO_URII)
db = client.get_database('easybali')
order_collection = db["orders-summary"]
villa_code_collection = db['villa-codes']