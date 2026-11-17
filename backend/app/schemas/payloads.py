from pydantic import BaseModel
from typing import Optional

class SchoolUpdatePayload(BaseModel):
    secret: str
    phone_number: str
    student_id: str
    name: str
    fees_due: str
    attendance: str
    latest_grade: str
    send_sms: Optional[bool] = True
    sms_custom_message: Optional[str] = None
