from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from ..models.user import create_user, get_user_by_id, update_user_preferences
from ..utils.logger import log_info, log_error
from ..utils.encryption import anonymize_user_id

router = APIRouter(prefix="/users", tags=["Users"])

class UserCreateRequest(BaseModel):
    phone: Optional[str] = None
    district: str
    language: str = "en-IN"
    age: Optional[int] = None

class UserPreferences(BaseModel):
    district: Optional[str] = None
    language: Optional[str] = None
    receive_alerts: Optional[bool] = None

@router.post("")
async def create_user_endpoint(request: UserCreateRequest):
    try:
        user_data = {
            "district": request.district,
            "language": request.language,
            "age": request.age,
            "created_at": datetime.utcnow()
        }
        
        if request.phone:
            user_data["phone"] = request.phone
        
        user_id = await create_user(user_data)
        anon_user_id = anonymize_user_id(user_id)
        
        log_info(f"Created new user: {anon_user_id}")
        
        return {
            "user_id": anon_user_id,
            "message": "User created successfully"
        }
        
    except Exception as e:
        log_error(f"User creation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating user")

@router.get("/{user_id}")
async def get_user_endpoint(user_id: str):
    try:
        anon_user_id = anonymize_user_id(user_id)
        user = await get_user_by_id(anon_user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "user_id": anon_user_id,
            "district": user.get("district"),
            "language": user.get("language"),
            "age": user.get("age"),
            "created_at": user.get("created_at")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        log_error(f"User fetch error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching user")

@router.put("/{user_id}/preferences")
async def update_user_preferences_endpoint(user_id: str, preferences: UserPreferences):
    try:
        anon_user_id = anonymize_user_id(user_id)
        updated = await update_user_preferences(anon_user_id, preferences.dict(exclude_unset=True))
        
        if not updated:
            raise HTTPException(status_code=404, detail="User not found")
        
        log_info(f"Updated preferences for user: {anon_user_id}")
        
        return {"message": "Preferences updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        log_error(f"Preferences update error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating preferences")