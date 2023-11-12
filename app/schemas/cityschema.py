# schemas/city_schema.py
from app import ma
from app.models.city import City

class CitySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = City
        load_instance = True
