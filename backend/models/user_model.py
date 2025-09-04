from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserModel(BaseModel):
    email: EmailStr
    username: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
