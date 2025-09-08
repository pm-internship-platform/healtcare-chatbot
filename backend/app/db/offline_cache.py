import json
from pathlib import Path
from ..utils.logger import log_info, log_error

CACHE_DIR = Path("data/cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

async def get_cached_disease_info(disease: str):
    cache_file = CACHE_DIR / f"disease_{disease.lower()}.json"
    
    if cache_file.exists():
        try:
            with open(cache_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            log_error(f"Cache read error for {disease}: {str(e)}")
    
    # Default disease information
    default_info = {
        "symptoms": "Fever, fatigue, and other general symptoms. Consult a doctor for accurate diagnosis.",
        "prevention": "Maintain good hygiene, avoid contaminated water/food, use protective measures.",
        "treatment": "Rest, hydration, and medical consultation. Follow doctor's advice for specific treatment."
    }
    
    # Save to cache
    try:
        with open(cache_file, 'w') as f:
            json.dump(default_info, f)
    except Exception as e:
        log_error(f"Cache write error for {disease}: {str(e)}")
    
    return default_info

async def get_cached_vaccination_schedule(age: int):
    cache_file = CACHE_DIR / "vaccination_schedule.json"
    
    if cache_file.exists():
        try:
            with open(cache_file, 'r') as f:
                schedules = json.load(f)
                return schedules.get(str(age), schedules["default"])
        except Exception as e:
            log_error(f"Vaccination cache read error: {str(e)}")
    
    # Default vaccination schedule
    default_schedules = {
        "0": "BCG, Hepatitis B-1, OPV-0 at birth",
        "6": "DPT-1, Hepatitis B-2, Hib-1, IPV-1, PCV-1, Rota-1 at 6 weeks",
        "10": "DPT-2, Hepatitis B-3, Hib-2, IPV-2, PCV-2, Rota-2 at 10 weeks",
        "14": "DPT-3, Hepatitis B-4, Hib-3, IPV-3, PCV-3, Rota-3 at 14 weeks",
        "9": "Measles-Rubella-1, JE-1 at 9-12 months",
        "16": "DPT booster, Measles-Rubella-2, JE-2, OPV booster at 16-24 months",
        "default": "Consult your local health center for appropriate vaccination schedule"
    }
    
    # Save to cache
    try:
        with open(cache_file, 'w') as f:
            json.dump(default_schedules, f)
    except Exception as e:
        log_error(f"Vaccination cache write error: {str(e)}")
    
    return default_schedules.get(str(age), default_schedules["default"])