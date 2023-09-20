from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from app.base.enums import JobCategoryEnum


class JobSchema(Schema):
    job_id = fields.UUID(dump_only=True)
    title = fields.String(required=True)
    location = fields.String(required=True)
    positions = fields.Integer(required=True)
    category = EnumField(JobCategoryEnum, required=True)
    employer_id = fields.UUID(required=True)
