import africastalking
from flask_restful import Resource
from flask import request
from app.sms.model import SMSMessage
from app.users.model import User
from app.sms.schema import SMSSchema
from flask import Response
from app.base.models import save
from app.users.resource import UserResource
from app.at_utils.utils import SMSSender
from db import db
from app.jobs.resource import JobsResource


class IncomingSMSResource(Resource):
    model = SMSMessage
    schema = SMSSchema()
    sms_sender = SMSSender()

    def post(self):
        data = request.form.to_dict()
        sms_data = {}
        sms_data['sms_id'] = data['id']
        sms_data['date'] = data['date']
        sms_data['sender'] = data['from']
        sms_data['text'] = data['text']
        item = self.model(**sms_data)

        try:
            save(item)
            if item.text.lower() == 'register':
                message = "Welcome to Kazi. Reply with 1 for Jobseeker or 2 " \
                          "for Employer"
                self.sms_sender.send_sms([item.sender], message)
            if item.text == "1" or item.text == '2':
                message = "Reply with your details in the following format: " \
                          "Name # ID Number # Location"
                self.sms_sender.send_sms([item.sender], message)
            if "#" in item.text:
                role = self.get_role(item.sender)
                self.handle_registration(item, role)
            if item.text.lower() == "post":
                message = "Please reply with the category of the job you " \
                          "want to post below: \n" \
                          "A. CONSTRUCTION \n B. FARMING \n C. WAREHOUSE " \
                          "\nD. PLUMBING \n E. GENERAL"
                self.sms_sender.send_sms([item.sender], message)
            if item.text in ["A", "B", "C", "D", "E"]:
                message = "Post your  job details in this format: " \
                          "\n Title * Location * Positions"
                self.sms_sender.send_sms([item.sender], message)
            if "*" in item.text:
                job_details = item.text.split("*")
                job_details = [x.strip() for x in job_details]
                category = self.get_category(
                    self.get_previous_message(item.sender))
                employer_id = self.get_user_id(item.sender)
                job_data = {'title': job_details[0], 'location':
                    job_details[1], 'positions': int(job_details[2]),
                            'category': category, 'employer_id': employer_id}
                JobsResource().post_sms_job(job_data)
                message = "Job posted successfully"
                self.sms_sender.send_sms([item.sender], message)


        except Exception as e:
            print(e)
            return {"error": e.args}, 500
        return Response(status=200)

    def get_role(self, phone_number):
        session = db.session
        last_message = session.query(SMSMessage.text).filter(
            SMSMessage.sender == phone_number).order_by(
            SMSMessage.date.desc()).offset(1).first()
        return "JOBSEEKER" if last_message[0] == "1" else "EMPLOYER"

    def handle_registration(self, sms_message, role):
        details = sms_message.text.split("#")
        details = [x.strip() for x in details]
        user_data = {'name': details[0], 'phone_number': sms_message.sender,
                     'id_number': details[1], 'location': details[2],
                     'role': role}
        UserResource().register_sms_user(user_data)
        recipients = [sms_message.sender]
        message = "You are now registered on Kazi. welcome"
        self.sms_sender.send_sms(recipients, message)

    def get_category(self, text):
        map = {"A": "CONSTRUCTION", "B": "FARMING", "C": "WAREHOUSE",
               "D": "PLUMBING", "E": "GENERAL"}
        return map[text.upper()]

    def get_previous_message(self, phone_number):
        session = db.session
        return session.query(SMSMessage.text).filter(
            SMSMessage.sender == phone_number).order_by(
            SMSMessage.date.desc()).offset(1).first()[0]

    def get_user_id(self, phone_number):
        session = db.session
        return session.query(User.user_id).filter(
            User.phone_number == phone_number).first()[0]
