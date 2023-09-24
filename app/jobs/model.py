import uuid

from app.base.models import BaseModel
from sqlalchemy import (Column,
                        UUID,
                        String,
                        Integer,
                        Enum,
                        ForeignKey,
                        Date,
                        Boolean)
from app.base.enums import JobCategoryEnum
from datetime import date


class Job(BaseModel):
    __tablename__ = "job"
    job_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    title = Column(String, nullable=False)
    location = Column(String, nullable=False)
    positions = Column(Integer, nullable=False)
    category = Column(Enum(JobCategoryEnum), nullable=False)
    date = Column(Date, nullable=False, default=date.today())
    filled = Column(Boolean, nullable=False, default=False)
    employer_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"),
                         nullable=False)
    job_code = Column(String, nullable=False)


class JobApplicatioin(BaseModel):
    __tablename__ = "job_application"
    application_id = Column(UUID(as_uuid=True), primary_key=True,
                            default=uuid.uuid4())
    jobseeker_id = Column(UUID(as_uuid=True), nullable=False)
    job_id = Column(UUID(as_uuid=True), ForeignKey("job.job_id"),
                    nullable=False)
