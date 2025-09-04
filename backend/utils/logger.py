# app/utils/logger.py
import logging
import sys
from app.config import settings

def init_logging() -> logging.Logger:
    level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logger = logging.getLogger("ai_health")
    if logger.handlers:
        return logger
    handler = logging.StreamHandler(sys.stdout)
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    logger.setLevel(level)
    # configure sub-loggers
    for name in ("ai_health.db", "ai_health.openai", "ai_health.gemini", "ai_health.hf", "ai_health.rasa"):
        logging.getLogger(name).setLevel(level)
    return logger
