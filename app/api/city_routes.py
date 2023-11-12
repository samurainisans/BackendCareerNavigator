from flask import jsonify

from app.api.user_routes import api_blueprint
from app.models.city import City
from app.schemas.cityschema import CitySchema


@api_blueprint.route('/cities', methods=['GET'])
def get_cities():
    cities = City.query.all()
    cities_data = CitySchema(many=True).dump(cities)
    response = {
        "result": cities_data,
        "status_code": 200
    }
    return jsonify(response), 200
