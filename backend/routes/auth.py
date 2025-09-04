from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from ..services.user_service import UserService
from ..core.security import verify_token

router = APIRouter()

class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
async def register(payload: RegisterRequest):
    existing = await UserService.get_user_by_email(payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await UserService.create_user(payload.email, payload.username, payload.password)
    return {"ok": True, "user_id": str(user["_id"])}

@router.post("/login")
async def login(payload: LoginRequest):
    auth = await UserService.authenticate_user(payload.email, payload.password)
    if not auth:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": auth["access_token"], "user": {"email": auth["user"]["email"], "username": auth["user"]["username"]}}

def get_current_user(token: str = Depends(verify_token)):
    user_data = verify_token(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_data
