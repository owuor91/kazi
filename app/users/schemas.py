from marshmallow import fields, Schema
from marshmallow_enum import EnumField
from app.base.enums import RoleEnum


class UserSchema(Schema):
    user_id = fields.UUID(dump_only=True)
    name = fields.String(required=True)
    phone_number = fields.String(required=True)
    id_number = fields.String(required=True)
    location = fields.String(required=True)
    role = EnumField(RoleEnum)
