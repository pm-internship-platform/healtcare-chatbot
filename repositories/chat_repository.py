from datetime import datetime
from backend.services.db_service import db

async def save_chat(user_id: str, provider: str, user_message: str, bot_response: str, meta: dict = {}):
    doc = {
        "user_id": user_id,
        "provider": provider,
        "message": user_message,
        "response": bot_response,
        "meta": meta,
        "created_at": datetime.utcnow()
    }
    result = await db.db["chats"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc

async def get_user_chats(user_id: str, limit: int = 50):
    cursor = db.db["chats"].find({"user_id": user_id}).sort("created_at", -1).limit(limit)
    return await cursor.to_list(length=limit)