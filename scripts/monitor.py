#!/usr/bin/env python3
"""
Script to monitor backend and Rasa services
"""

import requests
import time
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('monitor.log'),
        logging.StreamHandler()
    ]
)

SERVICES = {
    "backend": "http://localhost:8000/health",
    "rasa": "http://localhost:5005/version",
    "rasa_actions": "http://localhost:5055/health"
}

def check_service(service_name, url):
    """Check if a service is running"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            logging.info(f"✅ {service_name} is running")
            return True
        else:
            logging.warning(f"⚠️ {service_name} returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ {service_name} is down: {str(e)}")
        return False

def main():
    """Main monitoring function"""
    logging.info("Starting service monitoring...")
    
    while True:
        logging.info(f"\n--- Service Check at {datetime.now()} ---")
        
        all_services_up = True
        
        for service_name, url in SERVICES.items():
            if not check_service(service_name, url):
                all_services_up = False
        
        if all_services_up:
            logging.info("All services are running normally!")
        else:
            logging.warning("Some services are experiencing issues!")
        
        # Wait before next check
        time.sleep(300)  # Check every 5 minutes

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Monitoring stopped by user")