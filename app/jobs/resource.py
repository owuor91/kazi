from app.base.resource import BaseResource
from app.jobs.model import Job
from app.jobs.schemas import JobSchema
from app.base.models import save


class JobsResource(BaseResource):
    model = Job
    schema = JobSchema()

    def post_sms_job(self, job_data):
        errors = self.schema.validate(job_data)
        if errors:
            return {"error": True, "errors": str(errors)}, 400
        item = self.model(**job_data)

        try:
            save(item)
            return self.schema.dump(item), 201
        except Exception as e:
            return {"error": e.args}, 500
