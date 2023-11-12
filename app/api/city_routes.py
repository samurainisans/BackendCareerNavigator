from flask import jsonify

from app.api.user_routes import api_blueprint
from app.models.city import City
from app.schemas.cityschema import CitySchema


@api_blueprint.route('/cities', methods=['GET'])
def get_cities():
    try:
        cities = City.query.all()
        if not cities:
            return jsonify({"error": "No cities found", "status_code": 404}), 404
        return jsonify({"result": CitySchema(many=True).dump(cities), "status_code": 200}), 200
    except Exception as e:
        return jsonify({"error": str(e), "status_code": 500}), 500

