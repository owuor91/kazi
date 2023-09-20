import africastalking
import os
from dotenv import load_dotenv

load_dotenv()


class SMSSender:
    def __init__(self):
        self.username = os.getenv('AT_USERNAME')
        self.api_key = os.getenv('AT_API_KEY')
        africastalking.initialize(self.username, self.api_key)
        self.sms_service = africastalking.SMSService(self.username,
                                                     self.api_key)

    def send_sms(self, recipients, message):
        try:
            response = self.sms_service.send(message=message,
                                             recipients=recipients)
            print(response)
        except Exception as exc:
            print(exc)
            return {"error": exc}, 500
