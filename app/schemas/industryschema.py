from app import ma
from app.models.industry import Industry

class IndustrySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Industry
        fields = ("industry_id", "title")
