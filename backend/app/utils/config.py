# backend/app/utils/config.py
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # MongoDB
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "health_chatbot"
    
    # API Keys
    OPENROUTER_API_KEY: str = "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"
    TWILIO_ACCOUNT_SID: str = "your_twilio_sid_here"
    TWILIO_AUTH_TOKEN: str = "your_twilio_token_here"
    WHATSAPP_NUMBER: str = "your_whatsapp_number_here"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # App Settings
    ENVIRONMENT: str = "development"
    ANONYMIZATION_SALT: str = "change_this_in_production"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

_settings = None

def get_settings():
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings