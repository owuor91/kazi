from marshmallow import Schema, fields


class SMSSchema(Schema):
    sms_id = fields.UUID(required=True)
    date = fields.DateTime(required=True)
    sender = fields.String(required=True)
    text = fields.String(required=True)
