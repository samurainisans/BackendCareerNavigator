from marshmallow import fields, post_load

from app import ma
from app.models.company import Company
from app.models.job import Job
from app.models.city import City
from app.schemas.cityschema import CitySchema
from app.models.worktype import WorkType
from app.models.employment import Employment
from app.schemas.companyschema import CompanySchema
from app.schemas.employmentschema import EmploymentSchema
from app.schemas.worktypeschema import WorkTypeSchema


class JobSchema(ma.SQLAlchemyAutoSchema):
    work_type = fields.Method("get_worktype")
    city = fields.Method("get_city")
    employment = fields.Method("get_employment")
    company = fields.Method("get_company")

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
            "conditions",
            "requirements",
            "work_variant",
            "options",
            "salary",
            "experience",
            "date_posted")
        load_instance = True

    def get_worktype(self, obj):
        work_type = WorkType.query.get(obj.type_id)
        return WorkTypeSchema().dump(work_type)

    def get_city(self, obj):
        city = City.query.get(obj.city_id)
        return CitySchema().dump(city)

    def get_employment(self, obj):
        employment = Employment.query.get(obj.employment_id)
        return EmploymentSchema().dump(employment)

    def get_company(self, obj):
        company = Company.query.get(obj.company_id)
        return CompanySchema().dump(company)
