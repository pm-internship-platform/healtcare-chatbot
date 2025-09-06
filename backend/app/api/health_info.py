from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ..services.gov_api_client import GovAPIClient
from ..services.analytics import OutbreakPredictor
from ..services.bhashini_client import BhashiniClient
from ..utils.logger import log_info, log_error

router = APIRouter(prefix="/health", tags=["Health Information"])

class OutbreakAlertRequest(BaseModel):
    district: str
    language: str = "en-IN"

@router.get("/outbreak-alerts/{district}")
async def get_outbreak_alerts(district: str, language: str = "en-IN"):
    try:
        gov_client = GovAPIClient()
        bhashini = BhashiniClient()
        predictor = OutbreakPredictor()
        
        alerts = await gov_client.get_health_alerts(district)
        predictions = await predictor.predict_outbreaks(district)
        
        combined_alerts = alerts + predictions
        
        if language.startswith(('or', 'hi')):
            translated_alerts = []
            for alert in combined_alerts:
                translated_alert = await bhashini.translate(
                    text=alert, 
                    source_lang="en", 
                    target_lang=language
                )
                translated_alerts.append(translated_alert)
            combined_alerts = translated_alerts
        
        log_info(f"Fetched outbreak alerts for {district} in {language}")
        
        return {
            "district": district,
            "alerts": combined_alerts,
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        log_error(f"Outbreak alerts error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching outbreak alerts")

@router.get("/disease-info/{disease}")
async def get_disease_info(disease: str, language: str = "en-IN"):
    try:
        from ..db.offline_cache import get_cached_disease_info
        
        bhashini = BhashiniClient()
        disease_info = await get_cached_disease_info(disease)
        
        if language.startswith(('or', 'hi')):
            translated_info = {}
            for key, value in disease_info.items():
                translated_value = await bhashini.translate(
                    text=value, 
                    source_lang="en", 
                    target_lang=language
                )
                translated_info[key] = translated_value
            disease_info = translated_info
        
        log_info(f"Fetched disease info for {disease} in {language}")
        
        return disease_info
        
    except Exception as e:
        log_error(f"Disease info error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching disease information")

@router.get("/vaccination-schedule")
async def get_vaccination_schedule(age: int, language: str = "en-IN"):
    try:
        from ..db.offline_cache import get_cached_vaccination_schedule
        
        bhashini = BhashiniClient()
        schedule = await get_cached_vaccination_schedule(age)
        
        if language.startswith(('or', 'hi')):
            translated_schedule = {}
            for key, value in schedule.items():
                translated_value = await bhashini.translate(
                    text=value, 
                    source_lang="en", 
                    target_lang=language
                )
                translated_schedule[key] = translated_value
            schedule = translated_schedule
        
        log_info(f"Fetched vaccination schedule for age {age} in {language}")
        
        return schedule
        
    except Exception as e:
        log_error(f"Vaccination schedule error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching vaccination schedule")