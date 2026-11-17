from fastapi import APIRouter, HTTPException, status
from app.schemas.payloads import SchoolUpdatePayload
from app.core.cache import STUDENT_CACHE
from app.services.africastalking_service import send_sms_alert
from app.config import settings

router = APIRouter()

@router.post("/webhook/update-student")
async def update_student_record(payload: SchoolUpdatePayload):
    """
    Webhook endpoint hit by Google Apps Script whenever school data changes.
    Updates the sub-10ms USSD cache and dispatches an instant SMS notification.
    """
    # Verify secret key to prevent unauthorized updates
    if payload.secret != settings.WEBHOOK_SECRET:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid security token."
        )

    # 1. Real-time update to in-memory USSD cache
    STUDENT_CACHE[payload.phone_number] = {
        "student_id": payload.student_id,
        "name": payload.name,
        "fees_due": payload.fees_due,
        "attendance": payload.attendance,
        "latest_grade": payload.latest_grade
    }

    # 2. Dispatch instant SMS alert if requested
    sms_result = None
    if payload.send_sms:
        message = payload.sms_custom_message or (
            f"MzaziRada Alert: {payload.name}'s records have been updated.\n"
            f"Fees Due: {payload.fees_due}\n"
            f"Attendance: {payload.attendance}\n"
            f"Dial {settings.AT_SHORTCODE} anytime for full details."
        )
        sms_result = send_sms_alert(phone_number=payload.phone_number, message=message)

    return {
        "status": "success",
        "message": f"Cache updated for {payload.name}",
        "sms_delivery": sms_result
    }
