from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

class SurveyModel(BaseModel):
    user_id: str
    answers: List[Dict[str, Any]]
    created_at: datetime = Field(default_factory=datetime.utcnow)
