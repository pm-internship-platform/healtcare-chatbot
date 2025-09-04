from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict

# Use absolute import for repository
from repositories.survey_repository import save_survey  

router = APIRouter()

class SurveyRequest(BaseModel):
    user_id: str
    answers: List[Dict]

@router.post("/submit")
async def submit_survey(payload: SurveyRequest):
    """
    Saves survey answers to the database.
    """
    # Call repository function to save survey
    doc = await save_survey(payload.user_id, payload.answers)
    return {"ok": True, "id": str(doc["_id"])}
