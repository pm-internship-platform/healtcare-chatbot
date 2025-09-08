import hashlib
import os
from ..utils.config import get_settings

settings = get_settings()

def anonymize_user_id(user_id: str) -> str:
    """Anonymize user ID using SHA-256 hashing with salt"""
    salt = settings.ANONYMIZATION_SALT
    return hashlib.sha256(f"{user_id}{salt}".encode()).hexdigest()