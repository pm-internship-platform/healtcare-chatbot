from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ..services.openai_service import OpenAIService
from ..services.gemini_service import GeminiService
from ..services.huggingface_service import HuggingFaceService
from ..services.rasa_service import RasaService

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    provider: str = "openai"  # openai | gemini | huggingface | rasa

@router.post("/")
async def chat(req: ChatRequest):
    if req.provider == "openai":
        return {"reply": await OpenAIService().chat(req.message)}
    elif req.provider == "gemini":
        return {"reply": await GeminiService().chat(req.message)}
    elif req.provider == "huggingface":
        return {"reply": await HuggingFaceService().chat(req.message)}
    elif req.provider == "rasa":
        return {"reply": await RasaService().chat(req.message)}
    return {"error": "Invalid provider"}
