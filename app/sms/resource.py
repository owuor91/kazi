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
from app.jobs.resource import JobsResource, JobApplicationResource
from app.jobs.model import Job
from sqlalchemy import and_
from datetime import date
from app.base.enums import RoleEnum
from uuid import uuid4
from celery import shared_task
from app.base.exceptions import DatabaseError

sms_sender = SMSSender()
session = db.session


class IncomingSMSResource(Resource):
    model = SMSMessage
    schema = SMSSchema()

    def post(self):
        data = request.form.to_dict()
        sms_data = {}
        sms_data['sms_id'] = data['id']
        sms_data['date'] = data['date']
        sms_data['sender'] = data['from']
        sms_data['text'] = data['text']
        save_sms.delay(sms_data)
        handle_sms_async.delay(sms_data)
        return Response(status=200)


@shared_task(serializer='json')
def save_sms(sms_data):
    try:
        item = SMSMessage(**sms_data)
        save(item)
    except Exception as e:
        print(e)
        raise DatabaseError(e.args)


@shared_task
def handle_sms_async(sms_data):
    item = SMSMessage(**sms_data)
    if item.text.lower() == 'register':
        message = "Welcome to Kazi. Reply with 1 for Jobseeker or 2 " \
                  "for Employer"
        sms_sender.send_sms([item.sender], message)
    if item.text == "1" or item.text == '2':
        message = "Reply with your details in the following format: " \
                  "Name # ID Number # Location"
        sms_sender.send_sms([item.sender], message)
    if "#" in item.text:
        role = get_role(item.sender)
        handle_registration(item, role)
    if item.text.lower() == "post":
        message = "Please reply with the category of the job you " \
                  "want to post below: \n" \
                  "A. CONSTRUCTION \n B. FARMING \n C. WAREHOUSE " \
                  "\n D. PLUMBING \n E. GENERAL"
        sms_sender.send_sms([item.sender], message)
    if item.text in ["A", "B", "C", "D", "E"]:
        handle_job_category_message(sms_data)

    if "apply" in item.text.lower():
        handle_job_application(sms_data)

    if "*" in item.text:
        handle_job_posting(sms_data)


def get_role(phone_number):
    last_message = session.query(SMSMessage.text).filter(
        SMSMessage.sender == phone_number).order_by(
        SMSMessage.date.desc()).offset(1).first()
    return "JOBSEEKER" if last_message[0] == "1" else "EMPLOYER"


def handle_registration(sms_message, role):
    details = sms_message.text.split("#")
    details = [x.strip() for x in details]
    user_data = {'name': details[0], 'phone_number': sms_message.sender,
                 'id_number': details[1], 'location': details[2],
                 'role': role}
    UserResource().register_sms_user(user_data)
    recipients = [sms_message.sender]
    message = "You are now registered on Kazi. welcome"
    sms_sender.send_sms(recipients, message)


def get_category(text):
    map = {"A": "CONSTRUCTION", "B": "FARMING", "C": "WAREHOUSE",
           "D": "PLUMBING", "E": "GENERAL"}
    return map[text.upper()]


def get_previous_message(phone_number):
    return session.query(SMSMessage.text).filter(
        SMSMessage.sender == phone_number).order_by(
        SMSMessage.date.desc()).offset(1).first()[0]


def get_user_id(phone_number):
    return session.query(User.user_id).filter(
        User.phone_number == phone_number).first()[0]


def get_user_role(phone_number):
    return session.query(User.role).filter(
        User.phone_number == phone_number).first()[0]


def get_open_jobs_in_category(category):
    return session.query(Job).filter(
        and_(Job.category == category, Job.filled == False,
             Job.date == date.today())).all()


def count_jobs_in_category(category):
    return session.query(Job).filter(and_(Job.category == category,
                                          Job.date == date.today())).count()


def get_job_by_code(job_code):
    return session.query(Job).filter(
        and_(Job.job_code == job_code,
             Job.date == date.today())).first()


def handle_job_category_message(sms_data):
    item = SMSMessage(**sms_data)
    user_role = get_user_role(item.sender)
    if user_role.value == "EMPLOYER":
        message = "Post your  job details in this format: " \
                  "\n Title * Location * Positions"
        sms_sender.send_sms([item.sender], message)
    elif user_role.value == "JOBSEEKER":
        category = get_category(item.text)
        category_jobs = get_open_jobs_in_category(category)
        message = f"We have the following jobs under {category} " \
                  f"category. Please respond with the job you " \
                  f"want to apply to. e.g APPLY A1. \n"
        for job in category_jobs:
            message += f'\n{job.job_code}. {job.title}\n'
        sms_sender.send_sms([item.sender], message)


def handle_job_posting(sms_data):
    item = SMSMessage(**sms_data)
    job_details = item.text.split("*")
    job_details = [x.strip() for x in job_details]
    category_letter = get_previous_message(item.sender)
    category = get_category(category_letter)
    count = count_jobs_in_category(category) + 1
    job_code = f'{category_letter}{count}'
    employer_id = get_user_id(item.sender)
    job_data = {'title': job_details[0], 'location':
        job_details[1], 'positions': int(job_details[2]),
                'category': category, 'employer_id': employer_id,
                'date': str(date.today()), 'job_code': job_code,
                'job_id': str(uuid4())}
    JobsResource().post_sms_job(job_data)
    message = "Job posted successfully"
    sms_sender.send_sms([item.sender], message)


def handle_job_application(sms_data):
    item = SMSMessage(**sms_data)
    user_id = get_user_id(item.sender)
    code = item.text.split(' ')[1].upper()
    job = get_job_by_code(code)
    application = {"jobseeker_id": user_id, "job_id": str(
        job.job_id), "application_id": str(uuid4())}
    JobApplicationResource().post_sms_application(application)
    message = f'You have successfully applied to {job.title}. ' \
              f'The employer will contact you soon'
    sms_sender.send_sms([item.sender], message)


class JobNotificationResource(Resource):
    sms_sender = SMSSender()

    def post(self):
        jobseekers = self.get_all_jobseekers()
        jobseekers = [str(x[0]) for x in jobseekers]
        job_categories = self.get_categories_with_jobs()
        job_categories = [str(jc[0].value) for jc in job_categories]
        template = 'We have jobs in the following categories ' \
                   'today. Reply with the category letter to see available ' \
                   'jobs \n'

        cat_map = {"CONSTRUCTION": "A",
                   "FARMING": "B",
                   "WAREHOUSE": "C",
                   "PLUMBING": "D",
                   "GENERAL": "E", }
        for jc in job_categories:
            letter = cat_map.get(jc)
            template += f'{letter}. {jc} \n'

        self.sms_sender.send_sms(jobseekers, template)
        return {"status": "success"}, 200

    def get_categories_with_jobs(self):
        session = db.session
        return session.query(Job.category).filter(and_(
            Job.filled == False,
            Job.date == date.today()
        )).distinct().all()

    def get_all_jobseekers(self):
        session = db.session
        return session.query(User.phone_number).filter(
            User.role == RoleEnum.JOBSEEKER.value).all()
