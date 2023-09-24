from flask import Flask
from flask_restful import Api
from db import db
from app.users.resource import UserResource
from app.sms.resource import IncomingSMSResource, JobNotificationResource
from app.jobs.resource import JobsResource
from make_celery import make_celery


def create_app():
    app = Flask(__name__)
    api = Api(app)

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql+psycopg2:///kazi"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    api.add_resource(UserResource, "/users/register")
    api.add_resource(IncomingSMSResource, "/sms/inbox")
    api.add_resource(JobsResource, "/jobs")
    api.add_resource(JobNotificationResource, "/jobs-notification")

    celery = make_celery(app)
    celery.set_default()

    return app, celery


app, celery = create_app()
if __name__ == "__main__":
    app.run(debug=True, port=8080)
