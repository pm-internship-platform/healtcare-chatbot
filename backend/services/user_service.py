from passlib.context import CryptContext
from datetime import datetime
from ..services.db_service import db
from ..core.security import create_access_token, verify_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    @staticmethod
    async def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    async def verify_password(password: str, hashed: str) -> bool:
        return pwd_context.verify(password, hashed)

    @staticmethod
    async def create_user(email: str, username: str, password: str):
        hashed = await UserService.hash_password(password)
        doc = {
            "email": email,
            "username": username,
            "hashed_password": hashed,
            "is_active": True,
            "created_at": datetime.utcnow()
        }
        result = await db.db["users"].insert_one(doc)
        doc["_id"] = result.inserted_id
        return doc

    @staticmethod
    async def authenticate_user(email: str, password: str):
        user = await db.db["users"].find_one({"email": email})
        if not user:
            return None
        if not await UserService.verify_password(password, user["hashed_password"]):
            return None
        await db.db["users"].update_one({"_id": user["_id"]}, {"$set": {"last_login": datetime.utcnow()}})
        token = create_access_token({"sub": str(user["_id"]), "email": user["email"]})
        return {"user": user, "access_token": token}

    @staticmethod
    async def get_user(user_id: str):
        from bson import ObjectId
        return await db.db["users"].find_one({"_id": ObjectId(user_id)})
