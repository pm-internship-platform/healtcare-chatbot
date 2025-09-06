# backend/app/services/fallback_responder.py
"""
Simple rule-based responder for when AI services are unavailable
"""
from ..utils.logger import log_info

class FallbackResponder:
    def __init__(self):
        self.responses = {
            "greeting": [
                "Hello! I'm your Odisha Health Assistant. How can I help you today?",
                "Hi there! I can help with health information. What would you like to know?",
                "Welcome! I provide health information and advice. What can I help you with?"
            ],
            "symptoms": {
                "dengue": "Dengue symptoms: high fever, severe headache, pain behind eyes, muscle/joint pain, rash, mild bleeding.",
                "malaria": "Malaria symptoms: fever, chills, headache, nausea, vomiting, muscle pain, fatigue.",
                "covid": "COVID-19 symptoms: fever, cough, tiredness, loss of taste/smell, sore throat, headache.",
                "typhoid": "Typhoid symptoms: sustained high fever, weakness, stomach pain, headache, loss of appetite.",
                "default": "Common illness symptoms may include fever, fatigue, pain, or digestive issues. For specific symptoms, please consult a healthcare provider."
            },
            "prevention": {
                "dengue": "Prevent dengue: Use mosquito nets, repellents, wear protective clothing, eliminate standing water.",
                "malaria": "Prevent malaria: Sleep under insecticide-treated nets, use mosquito repellents, take prophylactic drugs if recommended.",
                "default": "General prevention: Maintain good hygiene, drink clean water, eat nutritious food, get vaccinated, and avoid contact with sick people."
            },
            "vaccination": "Vaccination schedule: Birth (BCG, HepB), 6 weeks (DPT, polio, Hib), 10 weeks, 14 weeks, 9-12 months (measles), 16-24 months (booster). Consult local health center for exact dates.",
            "general": [
                "I can help you with information about diseases, symptoms, prevention, and vaccinations.",
                "You can ask me about health topics like dengue, malaria, COVID-19, or vaccination schedules.",
                "I provide health information for Odisha residents. What specific health question do you have?"
            ]
        }
    
    async def get_response(self, message: str):
        message_lower = message.lower()
        
        # Greetings
        if any(word in message_lower for word in ["hello", "hi", "hey", "namaste", "namaskar"]):
            import random
            return random.choice(self.responses["greeting"])
        
        # Symptoms queries
        elif any(word in message_lower for word in ["symptom", "laksan", "sign", "feel", "hurt", "pain"]):
            for disease, response in self.responses["symptoms"].items():
                if disease in message_lower and disease != "default":
                    return response
            return self.responses["symptoms"]["default"]
        
        # Prevention queries
        elif any(word in message_lower for word in ["prevent", "roktham", "avoid", "protection", "safe"]):
            for disease, response in self.responses["prevention"].items():
                if disease in message_lower and disease != "default":
                    return response
            return self.responses["prevention"]["default"]
        
        # Vaccination queries
        elif any(word in message_lower for word in ["vaccine", "vaccination", "tika", "immunization"]):
            return self.responses["vaccination"]
        
        # Specific disease queries
        elif "dengue" in message_lower:
            return "Dengue is a mosquito-borne viral disease. Symptoms include high fever, severe headache, and joint pain. Prevention involves mosquito control and protection."
        
        elif "malaria" in message_lower:
            return "Malaria is caused by parasites transmitted through mosquito bites. Symptoms include fever, chills, and sweating. Use mosquito nets and repellents for prevention."
        
        elif "covid" in message_lower or "corona" in message_lower:
            return "COVID-19 is a respiratory illness. Prevent spread through vaccination, masks, hand washing, and social distancing."
        
        # Default response
        else:
            import random
            return random.choice(self.responses["general"])