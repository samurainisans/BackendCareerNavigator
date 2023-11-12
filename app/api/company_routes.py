from flask import jsonify, request

from app import db
from app.api.user_routes import api_blueprint
from app.models.company import Company
from app.schemas.companyschema import CompanySchema


@api_blueprint.route('/companies', methods=['GET'])
def get_companies():
    companies = Company.query.all()
    return jsonify(CompanySchema(many=True).dump(companies))


@api_blueprint.route('/companies', methods=['POST'])
def add_company():
    company_data = request.json
    company = CompanySchema().load(company_data)
    db.session.add(company)
    db.session.commit()
    return jsonify(CompanySchema().dump(company)), 201


@api_blueprint.route('/companies/<int:company_id>', methods=['PUT'])
def update_company(company_id):
    company_data = request.json
    company = Company.query.get_or_404(company_id)
    company = CompanySchema().load(company_data, instance=company)
    db.session.commit()
    return jsonify(CompanySchema().dump(company))
