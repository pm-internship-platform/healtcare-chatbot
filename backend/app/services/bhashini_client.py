import httpx
import json
from ..utils.logger import log_info, log_error
from ..utils.config import get_settings

settings = get_settings()

class BhashiniClient:
    def __init__(self):
        self.api_url = "https://api.bhashini.gov.in/services/translation"
        self.api_key = settings.BHASHINI_API_KEY
    
    async def translate(self, text: str, source_lang: str = "en", target_lang: str = "or"):
        if source_lang == target_lang:
            return text
            
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "text": text,
                "sourceLanguage": source_lang,
                "targetLanguage": target_lang
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(self.api_url, json=payload, headers=headers, timeout=30.0)
                response.raise_for_status()
                
                data = response.json()
                return data.get('translatedText', text)
                
        except Exception as e:
            log_error(f"Bhashini API error: {str(e)}")
            return text  # Return original text if translation fails