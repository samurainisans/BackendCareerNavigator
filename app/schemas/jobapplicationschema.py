from marshmallow import fields

from app import ma
from app.models.job import Job
from app.models.jobapplication import JobApplication
from app.models.user import User


class JobApplicationSchema(ma.SQLAlchemyAutoSchema):
    job = fields.Method("get_job")
    user = fields.Method("get_user")

    class Meta:
        model = JobApplication
        fields = ("application_id",
                  "job",
                  "user",
                  "resume",
                  "cover_letter",
                  "application_date",
                  "status")

    def get_job(self, obj):
        from app.schemas.jobschema import JobSchema
        job = Job.query.get(obj.job_id)
        return JobSchema().dump(job)

    def get_user(self, obj):
        from app.schemas.userschema import UserSchema
        user = User.query.get(obj.user_id)
        return UserSchema().dump(user)
