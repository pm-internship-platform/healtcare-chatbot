from backend.services.db_service import db

async def save_survey(user_id: str, answers: list):
    doc = {
        "user_id": user_id,
        "answers": answers,
        "created_at": datetime.utcnow()
    }
    doc["_id"] = result.insert_one(doc)
    return doc

async def get_user_surveys(user_id: str, limit: int = 50):
    cursor = db.db["surveys"].find({"user_id": user_id}).sort("created_at", -1).limit(limit)
    return await cursor.to_list(length=limit)