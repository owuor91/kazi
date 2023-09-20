import uuid

from app.base.models import BaseModel
from sqlalchemy import Column, UUID, String, Integer, Enum, ForeignKey
from app.base.enums import JobCategoryEnum


class Job(BaseModel):
    __tablename__ = "job"
    job_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    title = Column(String, nullable=False)
    location = Column(String, nullable=False)
    positions = Column(Integer, nullable=False)
    category = Column(Enum(JobCategoryEnum), nullable=False)
    employer_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"),
                         nullable=False)
