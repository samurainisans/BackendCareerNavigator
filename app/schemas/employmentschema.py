from app import ma
from app.models.employment import Employment

class EmploymentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Employment
        load_instance = True
