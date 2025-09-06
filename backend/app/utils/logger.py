import logging
import sys
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(LOG_DIR / "app.log")
        ]
    )

def log_info(message: str):
    logging.info(message)

def log_error(message: str):
    logging.error(message)

def log_warning(message: str):
    logging.warning(message)

def log_debug(message: str):
    logging.debug(message)