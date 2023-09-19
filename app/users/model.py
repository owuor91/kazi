from app.base.models import BaseModel
from sqlalchemy import Column, UUID, String, Enum
import uuid
from app.base.enums import RoleEnum


class User(BaseModel):
    __tablename__ = "user"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)
    phone_number = Column(String(50), nullable=False, unique=True)
    id_number = Column(String(50), nullable=False, unique=True)
    location = Column(String(50), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
