# schemas/company_schema.py
from app import ma
from app.models.company import Company
from app.models.industry import Industry
from app.schemas.industryschema import IndustrySchema
from marshmallow import fields


class CompanySchema(ma.SQLAlchemyAutoSchema):
    industry = fields.Method("get_industry")

    class Meta:
        model = Company
        fields = ("company_id", "name", "description", "logo_url", "industry")

    def get_industry(self, obj):
        industry = Industry.query.get(obj.industry_id)
        return IndustrySchema().dump(industry)
