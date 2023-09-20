from app.base.models import BaseModel
from sqlalchemy import Column, UUID, String, DateTime


class SMSMessage(BaseModel):
    __tablename__ = "sms_inbox"
    sms_id = Column(UUID(as_uuid=True), primary_key=True)
    date = Column(DateTime, nullable=False)
    sender = Column(String, nullable=False)
    text = Column(String, nullable=False)
