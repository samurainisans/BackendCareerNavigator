from app import ma
from app.models.worktype import WorkType

class WorkTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WorkType
        load_instance = True
