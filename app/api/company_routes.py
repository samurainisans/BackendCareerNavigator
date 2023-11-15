from flask import jsonify, request
from flask_jwt_extended import jwt_required, JWTManager
from marshmallow import ValidationError

from app import db
from app.api.user_routes import api_blueprint
from app.models.company import Company
from app.models.industry import Industry
from app.schemas.companyschema import CompanySchema

jwt = JWTManager()

@api_blueprint.route('/companies', methods=['GET'])
def get_companies():
    try:
        companies = Company.query.all()
        if not companies:
            return jsonify({"error": "No companies found", "status_code": 404}), 404
        return jsonify({"result": CompanySchema(many=True).dump(companies), "status_code": 200}), 200
    except Exception as e:
        return jsonify({"error": str(e), "status_code": 500}), 500


@api_blueprint.route('/companies', methods=['POST'])
@jwt_required()
def add_company():
    try:
        company_data = request.json
        industry_data = company_data.pop('industry')
        industry = Industry(**industry_data)
        db.session.merge(industry)
        db.session.flush()
        company_data['industry_id'] = industry.industry_id
        company = Company(**company_data)
        db.session.merge(company)
        db.session.commit()
        return jsonify({"msg": "Company added successfully", "status_code": 201}), 201
    except ValidationError as ve:
        return jsonify({"msg": str(ve), "status_code": 400}), 400
    except Exception as e:
        return jsonify({"msg": str(e), "status_code": 500}), 500


@api_blueprint.route('/companies/<int:company_id>', methods=['PUT'])
@jwt_required()
def update_company(company_id):
    try:
        company_data = request.json
        company = Company.query.get(company_id)
        if not company:
            return jsonify({"msg": "Company not found", "status_code": 404}), 404
        company = CompanySchema().load(company_data, instance=company, partial=True)
        db.session.commit()
        return jsonify({"msg": "Company updated successfully", "status_code": 200}), 200
    except ValidationError as ve:
        return jsonify({"msg": str(ve), "status_code": 400}), 400
    except Exception as e:
        return jsonify({"msg": str(e), "status_code": 500}), 500
