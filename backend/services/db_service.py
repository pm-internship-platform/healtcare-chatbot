# backend/services/db_service.py

from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings  # import the settings instance

# Use settings.MONGO_URI instead of a standalone MONGO_URI
MONGO_URI = settings.MONGO_URI
MONGO_DB = settings.MONGO_DB

db_client = AsyncIOMotorClient(MONGO_URI)
db = db_client[MONGO_DB]
