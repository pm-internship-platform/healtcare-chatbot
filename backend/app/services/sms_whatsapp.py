from twilio.rest import Client
from ..utils.logger import log_info, log_error
from ..utils.config import get_settings

settings = get_settings()

class TwilioClient:
    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        self.whatsapp_number = settings.WHATSAPP_NUMBER
    
    async def send_whatsapp_message(self, to_number: str, message: str):
        try:
            message = self.client.messages.create(
                body=message,
                from_=f'whatsapp:{self.whatsapp_number}',
                to=f'whatsapp:{to_number}'
            )
            log_info(f"WhatsApp message sent to {to_number}: {message.sid}")
            return True
        except Exception as e:
            log_error(f"WhatsApp sending error: {str(e)}")
            return False
    
    async def send_sms(self, to_number: str, message: str):
        try:
            message = self.client.messages.create(
                body=message,
                from_=self.whatsapp_number,  # Using the same number for SMS
                to=to_number
            )
            log_info(f"SMS sent to {to_number}: {message.sid}")
            return True
        except Exception as e:
            log_error(f"SMS sending error: {str(e)}")
            return False

# Global instance
twilio_client = TwilioClient()

async def send_whatsapp_message(to_number: str, message: str):
    return await twilio_client.send_whatsapp_message(to_number, message)

async def send_sms(to_number: str, message: str):
    return await twilio_client.send_sms(to_number, message)