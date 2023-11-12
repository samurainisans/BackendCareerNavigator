from marshmallow import fields

from app import ma
from app.models.job import Job
from app.models.city import City
from app.schemas.cityschema import CitySchema
from app.models.worktype import WorkType
from app.models.employment import Employment
from app.schemas.employmentschema import EmploymentSchema
from app.schemas.worktypeschema import WorkTypeSchema


class JobSchema(ma.SQLAlchemyAutoSchema):
    work_type = fields.Method("get_worktype")
    city = fields.Method("get_city")
    employment = fields.Method("get_employment")

    class Meta:
        model = Job
        fields = (
            "job_id",
            "company",
            "work_type",
            "city",
            "employment",
            "title",
            "description",
            "requirements",
            "salary",
            "experience",
            "date_posted")

    def get_worktype(self, obj):
        work_type = WorkType.query.get(obj.type_id)
        return WorkTypeSchema().dump(work_type)

    def get_city(self, obj):
        city = City.query.get(obj.city_id)
        return CitySchema().dump(city)

    def get_employment(self, obj):
        employment = Employment.query.get(obj.employment_id)
        return EmploymentSchema().dump(employment)
