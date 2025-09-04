from pydantic import BaseModel, Field
from typing import Dict, Any
from datetime import datetime

class ChatModel(BaseModel):
    user_id: str
    provider: str
    message: str
    response: str
    meta: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
