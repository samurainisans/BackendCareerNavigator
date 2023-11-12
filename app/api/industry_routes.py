from flask import jsonify

from app.api.user_routes import api_blueprint
from app.models.industry import Industry
from app.schemas.industryschema import IndustrySchema


@api_blueprint.route('/industries', methods=['GET'])
def get_industries():
    industries = Industry.query.all()
    return jsonify(IndustrySchema(many=True).dump(industries))
