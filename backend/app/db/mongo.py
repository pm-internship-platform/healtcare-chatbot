from motor.motor_asyncio import AsyncIOMotorClient
from ..utils.config import get_settings
from ..utils.logger import log_info, log_error

settings = get_settings()

# MongoDB connection
client = None
db = None

# Collections
users_collection = None
conversations_collection = None
quiz_results_collection = None
quizzes_collection = None

async def connect_to_mongo():
    global client, db, users_collection, conversations_collection, quiz_results_collection, quizzes_collection
    
    try:
        client = AsyncIOMotorClient(settings.MONGO_URI)
        db = client[settings.MONGO_DB_NAME]
        
        # Initialize collections
        users_collection = db.users
        conversations_collection = db.conversations
        quiz_results_collection = db.quiz_results
        quizzes_collection = db.quizzes
        
        # Create indexes
        await users_collection.create_index("user_id", unique=True)
        await users_collection.create_index("phone", unique=True, sparse=True)
        await conversations_collection.create_index([("user_id", 1), ("timestamp", -1)])
        await quiz_results_collection.create_index([("user_id", 1), ("timestamp", -1)])
        
        log_info("Connected to MongoDB successfully")
        
    except Exception as e:
        log_error(f"MongoDB connection error: {str(e)}")
        raise

async def close_mongo_connection():
    if client:
        client.close()
        log_info("MongoDB connection closed")