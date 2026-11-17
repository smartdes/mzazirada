import africastalking
from app.config import settings

# Initialize Africa's Talking SDK
africastalking.initialize(username=settings.AT_USERNAME, api_key=settings.AT_API_KEY)
sms_service = africastalking.SMS

def send_sms_alert(phone_number: str, message: str) -> dict:
    """
    Sends an SMS notification to a parent's phone number via Africa's Talking.
    """
    try:
        response = sms_service.send(
            message=message,
            recipients=[phone_number]
        )
        return {"status": "success", "response": response}
    except Exception as e:
        return {"status": "error", "message": str(e)}
