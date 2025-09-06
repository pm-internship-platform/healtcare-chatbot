from bson import ObjectId
from datetime import datetime
from ..db.mongo import users_collection
from ..utils.logger import log_info, log_error

async def create_user(user_data: dict):
    try:
        result = await users_collection.insert_one(user_data)
        return str(result.inserted_id)
    except Exception as e:
        log_error(f"User creation error: {str(e)}")
        raise

async def get_user_by_id(user_id: str):
    try:
        user = await users_collection.find_one({"user_id": user_id})
        return user
    except Exception as e:
        log_error(f"User fetch error: {str(e)}")
        return None

async def update_user_preferences(user_id: str, preferences: dict):
    try:
        result = await users_collection.update_one(
            {"user_id": user_id},
            {"$set": {**preferences, "updated_at": datetime.utcnow()}}
        )
        return result.modified_count > 0
    except Exception as e:
        log_error(f"Preferences update error: {str(e)}")
        return False

async def get_user_by_phone(phone: str):
    try:
        user = await users_collection.find_one({"phone": phone})
        return user
    except Exception as e:
        log_error(f"User fetch by phone error: {str(e)}")
        return None