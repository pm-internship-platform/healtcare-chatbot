# backend/app/models/conversation.py
from datetime import datetime
from ..db.mongo import conversations_collection
from ..utils.logger import log_info, log_error

async def save_conversation(user_id: str, message: str, response: str, language: str, source: str):
    try:
        # Check if collection is initialized
        if conversations_collection is None:
            log_error("Conversations collection is not initialized")
            return False
            
        conversation = {
            "user_id": user_id,
            "message": message,
            "response": response,
            "language": language,
            "source": source,
            "timestamp": datetime.utcnow()
        }
        result = await conversations_collection.insert_one(conversation)
        log_info(f"Conversation saved for user {user_id}, ID: {result.inserted_id}")
        return True
    except Exception as e:
        log_error(f"Conversation save error: {str(e)}")
        return False

async def get_conversation_history(user_id: str, limit: int = 20):
    try:
        if conversations_collection is None:
            log_error("Conversations collection is not initialized")
            return []
            
        conversations = await conversations_collection.find(
            {"user_id": user_id}
        ).sort("timestamp", -1).limit(limit).to_list(length=limit)
        return conversations
    except Exception as e:
        log_error(f"Conversation history fetch error: {str(e)}")
        return []