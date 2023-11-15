from marshmallow import fields

from app import ma
from app.models.job import Job
from app.models.jobapplication import JobApplication
from app.models.resume import Resume


class JobApplicationSchema(ma.SQLAlchemyAutoSchema):
    job = fields.Method("get_job")
    resume = fields.Method("get_resume")

    class Meta:
        model = JobApplication
        fields = ("application_id",
                  "job",
                  "resume",
                  "cover_letter",
                  "application_date",
                  "status")

    def get_job(self, obj):
        from app.schemas.jobschema import JobSchema
        job = Job.query.get(obj.job_id)
        if job is None:
            return None  # или другое подходящее значение
        return JobSchema().dump(job)

    def get_resume(self, obj):
        from app.schemas.resumeschema import ResumeSchema
        resume = Resume.query.get(obj.resume_id)
        if resume is None:
            return None  # или другое подходящее значение
        return ResumeSchema().dump(resume)
