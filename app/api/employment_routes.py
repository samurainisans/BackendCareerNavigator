from flask import jsonify

from app.api.user_routes import api_blueprint

from app.models.employment import Employment
from app.schemas.employmentschema import EmploymentSchema


@api_blueprint.route('/employments', methods=['GET'])
def get_employments():
    employments = Employment.query.all()
    return jsonify(EmploymentSchema(many=True).dump(employments))
