from fastapi import APIRouter, Form, Response
from app.core.state_machine import process_ussd_session

router = APIRouter()

@router.post("/ussd")
async def ussd_callback(
    sessionId: str = Form(...),
    serviceCode: str = Form(...),
    phoneNumber: str = Form(...),
    text: str = Form("")
):
    """
    Receives form-encoded USSD session callbacks from Africa's Talking and returns a sub-10ms plain-text CON/END response.
    """
    # Evaluate user state through in-memory FSM
    response_text = process_ussd_session(phone_number=phoneNumber, text=text)
    
    # Telecom gateways require text/plain format
    return Response(content=response_text, media_type="text/plain")
