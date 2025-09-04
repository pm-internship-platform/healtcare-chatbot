from fastapi import APIRouter
from pydantic import BaseModel
from ..services.health_service import get_disease_info

router = APIRouter()

class HealthResponse(BaseModel):
    info: str

@router.get("/disease/{name}", response_model=HealthResponse)
async def disease_info(name: str):
    info = await get_disease_info(name)
    return HealthResponse(info=info)
