# backend/app/services/rasa_client.py
import httpx
import json
from ..utils.logger import log_info, log_error
from ..utils.config import get_settings

settings = get_settings()

class RasaClient:
    def __init__(self):
        self.rasa_url = "http://localhost:5005/webhooks/rest/webhook"
    
    async def send_message(self, message: str):
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:  # Shorter timeout
                payload = {
                    "sender": "user",
                    "message": message
                }
                response = await client.post(self.rasa_url, json=payload)
                response.raise_for_status()
                
                rasa_data = response.json()
                if rasa_data:
                    return {
                        "text": rasa_data[0].get("text", "Sorry, I didn't understand that."),
                        "confidence": 0.8,
                        "intent": {"name": "general_query"}
                    }
                return {"text": "Sorry, I didn't understand that.", "confidence": 0.1}
                
        except httpx.RequestError as e:
            log_error(f"Rasa API connection error: {str(e)}")
            raise Exception("Rasa server not available")
        except Exception as e:
            log_error(f"Rasa API error: {str(e)}")
            raise Exception("Rasa processing error")