import httpx
import json
from ..utils.logger import log_info, log_error

class GovAPIClient:
    def __init__(self):
        self.base_url = "https://api.odisha.gov.in/health"
    
    async def get_health_alerts(self, district: str):
        # Mock implementation - replace with actual government API integration
        mock_alerts = {
            "bhubaneswar": [
                "Dengue outbreak reported in Bhubaneswar. Use mosquito nets and repellents.",
                "Heatwave alert: Temperatures expected to reach 42°C this week."
            ],
            "cuttack": [
                "Malaria cases increasing in Cuttack. Ensure proper sanitation.",
                "Free vaccination camp organized at SCB Medical College."
            ],
            "default": [
                "Stay updated with local health advisories.",
                "Drink plenty of water during summer months."
            ]
        }
        
        return mock_alerts.get(district.lower(), mock_alerts["default"])
    
    async def get_disease_info(self, disease: str):
        # Mock disease information
        disease_info = {
            "dengue": {
                "symptoms": "High fever, severe headache, pain behind eyes, muscle and joint pain, nausea, vomiting, swollen glands, rash",
                "prevention": "Use mosquito nets, wear protective clothing, use mosquito repellents, eliminate standing water",
                "treatment": "Rest, drink fluids, take acetaminophen for pain. Avoid aspirin. Seek medical attention for severe symptoms."
            },
            "malaria": {
                "symptoms": "Fever, chills, headache, nausea, vomiting, muscle pain, fatigue",
                "prevention": "Use insecticide-treated mosquito nets, indoor residual spraying, antimalarial medication for high-risk areas",
                "treatment": "Antimalarial drugs prescribed by healthcare provider based on parasite type and severity"
            },
            "covid": {
                "symptoms": "Fever, cough, fatigue, loss of taste or smell, sore throat, headache",
                "prevention": "Vaccination, mask-wearing, hand hygiene, physical distancing, ventilation",
                "treatment": "Rest, hydration, over-the-counter medications for symptoms. Seek medical care for severe symptoms."
            }
        }
        
        return disease_info.get(disease.lower(), {
            "symptoms": "Consult a healthcare provider for accurate information",
            "prevention": "Maintain good hygiene and follow public health advisories",
            "treatment": "Seek professional medical advice for proper treatment"
        })