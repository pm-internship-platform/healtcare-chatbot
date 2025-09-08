# backend/app/services/openrouter_client.py
import httpx
import json
from ..utils.logger import log_info, log_error
from ..utils.config import get_settings

settings = get_settings()

class OpenRouterClient:
    def __init__(self):
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.api_key = settings.OPENROUTER_API_KEY
    
    async def generate_response(self, prompt: str):
        # Don't attempt API call if no API key is set
        if not self.api_key or self.api_key == "your_openrouter_api_key_here":
            log_info("OpenRouter API key not configured, using fallback response")
            return self.get_fallback_response(prompt)
            
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "Odisha Health Chatbot"
            }
            
            # Use a valid model - try these options:
            valid_models = [
                "google/gemini-2.5-flash:free",
    "google/gemini-2.0-flash:free",
    "meta-llama/llama-3.1-8b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
    "meta-llama/llama-4-maverick:free",
    "moonshotai/kimi-vl-a3b-thinking:free",
    "nvidia/llama-3.1-nemotron-nano-8b-v1:free",
    "google/gemini-2.5-pro-exp-03-25:free",
    "mistralai/mistral-small-3.1-24b-instruct:free",
    "openrouter/optimus-alpha:free",
    "openrouter/quasar-alpha:free",
    "deepseek/deepseek-v3-base:free",
    "qwen/qwen2.5-vl-3b-instruct:free",
    "deepseek/deepseek-chat-v3-0324:free",
    "deepseek/deepseek-r1-zero:free",
    "nousresearch/deephermes-3-llama-3-8b-preview:free"
            ]
            
            payload = {
                "model": valid_models[0],  # Try the first valid model
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful health assistant for the people of Odisha, India. Provide accurate, clear health information in simple language. Be concise and helpful. Focus on preventive healthcare, disease symptoms, and vaccination information."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 500,
                "temperature": 0.7
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(self.api_url, json=payload, headers=headers, timeout=30.0)
                response.raise_for_status()
                
                data = response.json()
                return data['choices'][0]['message']['content'].strip()
                
        except httpx.HTTPStatusError as e:
            log_error(f"OpenRouter API HTTP error {e.response.status_code}: {e.response.text}")
            return self.get_fallback_response(prompt)
        except Exception as e:
            log_error(f"OpenRouter API error: {str(e)}")
            return self.get_fallback_response(prompt)
    
    def get_fallback_response(self, prompt: str):
        """Provide fallback responses when API is not available"""
        prompt_lower = prompt.lower()
        
        # Common health queries and their responses
        if any(word in prompt_lower for word in ["dengue", "denge"]):
            return "Dengue fever is a mosquito-borne viral infection. Symptoms include high fever, severe headache, pain behind the eyes, joint and muscle pain, and rash. Prevent dengue by using mosquito nets, repellents, and eliminating standing water where mosquitoes breed."
        
        elif any(word in prompt_lower for word in ["malaria", "maleria"]):
            return "Malaria is a serious mosquito-borne disease. Symptoms include fever, chills, headache, nausea, and vomiting. Use mosquito nets, wear protective clothing, and take anti-malarial medication if prescribed by a doctor."
        
        elif any(word in prompt_lower for word in ["vaccine", "vaccination", "tikakaran", "tika"]):
            return "Vaccination schedules are important for preventing diseases. Children should receive vaccines for BCG, Hepatitis B, DPT, polio, measles, and others according to the national immunization schedule. Consult your local health center for specific vaccination timing."
        
        elif any(word in prompt_lower for word in ["covid", "corona", "kovid"]):
            return "COVID-19 symptoms include fever, cough, fatigue, loss of taste or smell. Prevention methods include vaccination, mask-wearing, hand hygiene, and social distancing. If you have symptoms, consult a healthcare provider."
        
        elif any(word in prompt_lower for word in ["fever", "bukhara", "jvara"]):
            return "Fever can be caused by various infections. Rest, drink plenty of fluids, and take paracetamol if needed. If fever persists for more than 2 days or is very high, consult a doctor."
        
        elif any(word in prompt_lower for word in ["headache", "sirdardi", "munda bintha"]):
            return "For headaches, rest in a quiet dark room, apply a cool cloth to your forehead, and stay hydrated. Common pain relievers may help. If headaches are severe or frequent, consult a doctor."
        
        else:
            return "I'm here to help with health information. You can ask me about disease symptoms, prevention methods, vaccination schedules, or general health advice. For example, you could ask about dengue prevention, malaria symptoms, or vaccination information."