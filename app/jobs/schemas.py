from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from app.base.enums import JobCategoryEnum


class JobSchema(Schema):
    job_id = fields.UUID(required=True)
    title = fields.String(required=True)
    location = fields.String(required=True)
    positions = fields.Integer(required=True)
    category = EnumField(JobCategoryEnum, required=True)
    employer_id = fields.UUID(required=True)
    job_code = fields.String(required=True)
    date = fields.Date(required=True)


class JobApplicationSchema(Schema):
    application_id = fields.UUID(required=True)
    job_id = fields.UUID(required=True)
    jobseeker_id = fields.UUID(required=True)
