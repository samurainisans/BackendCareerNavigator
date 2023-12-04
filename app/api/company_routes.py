from flask import jsonify, request
from flask_jwt_extended import jwt_required, JWTManager, get_jwt_identity
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
        companies = Company.query.filter_by(status="accepted").all()
        if not companies:
            return jsonify({"error": "No companies found", "status_code": 404}), 404
        return jsonify({"result": CompanySchema(many=True).dump(companies), "status_code": 200}), 200
    except Exception as e:
        return jsonify({"error": str(e), "status_code": 500}), 500


@api_blueprint.route('/pending_companies', methods=['GET'])
def get_pending_companies():
    try:
        # Получаем компании с статусом "pending review"
        pending_companies = Company.query.filter_by(status='pending review').all()

        if not pending_companies:
            return jsonify({"error": "No pending companies found", "status_code": 404}), 404

        return jsonify({"result": CompanySchema(many=True).dump(pending_companies), "status_code": 200}), 200

    except Exception as e:
        return jsonify({"error": str(e), "status_code": 500}), 500

@api_blueprint.route('/companies', methods=['POST'])
def add_company():
    try:
        company_data = request.json
        industry_title = company_data.get('industry')

        # Проверяем, существует ли отрасль с указанным названием
        industry = Industry.query.filter_by(title=industry_title).first()

        if not industry:
            # Если отрасли нет, создаем новую отрасль
            industry = Industry(title=industry_title)
            db.session.add(industry)
            db.session.flush()

        # Добавляем компанию
        company = Company(
            name=company_data.get('name'),
            industry_id=industry.industry_id,
            description=company_data.get('description'),
            inn=company_data.get('inn'),
            ogrn=company_data.get('ogrn'),
            status='pending review'  # Устанавливаем начальный статус компании
        )

        db.session.add(company)
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
        industry_data = company_data.pop('industry')
        industry = Industry(**industry_data)
        db.session.merge(industry)
        db.session.commit()
        return jsonify({"msg": "Company updated successfully", "status_code": 200}), 200
    except ValidationError as ve:
        return jsonify({"msg": str(ve), "status_code": 400}), 400
    except Exception as e:
        return jsonify({"msg": str(e), "status_code": 500}), 500


@api_blueprint.route('/companies/<int:company_id>', methods=['PATCH'])
@jwt_required()
def update_company_field(company_id):
    try:
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        company = Company.query.filter_by(company_id=company_id).first()
        company.hr_id = user_id
        db.session.commit()

        return jsonify({"msg": "Company hr_id updated successfully", "status_code": 200}), 200

    except ValidationError as ve:
        return jsonify({"msg": str(ve), "status_code": 400}), 400
    except Exception as e:
        print(e)
        return jsonify({"msg": str(e), "status_code": 500}), 500


@api_blueprint.route('/companies/<int:company_id>/accept', methods=['PATCH'])
@jwt_required()
def accept_company(company_id):
    try:
        current_user = get_jwt_identity()
        admin_role = "admin"  # Укажите вашу роль администратора

        # Проверяем, что текущий пользователь является администратором
        if current_user.get('role') != admin_role:
            return jsonify({"error": "Access forbidden", "status_code": 403}), 403

        # Получаем компанию по идентификатору
        company = Company.query.filter_by(company_id=company_id).first()

        if not company:
            return jsonify({"msg": "Company not found", "status_code": 404}), 404

        # Обновляем статус компании на "accepted"
        company.status = "accepted"
        db.session.commit()

        return jsonify({"msg": "Company accepted successfully", "status_code": 200}), 200

    except Exception as e:
        return jsonify({"error": str(e), "status_code": 500}), 500


@api_blueprint.route('/companies/<int:company_id>/reject', methods=['PATCH'])
@jwt_required()
def reject_company(company_id):
    try:
        current_user = get_jwt_identity()
        admin_role = "admin"  # Укажите вашу роль администратора

        # Проверяем, что текущий пользователь является администратором
        if current_user.get('role') != admin_role:
            return jsonify({"error": "Access forbidden", "status_code": 403}), 403

        # Получаем компанию по идентификатору
        company = Company.query.filter_by(company_id=company_id).first()

        if not company:
            return jsonify({"msg": "Company not found", "status_code": 404}), 404

        # Обновляем статус компании на "denied"
        company.status = "denied"
        db.session.commit()

        return jsonify({"msg": "Company rejected successfully", "status_code": 200}), 200

    except Exception as e:
        return jsonify({"error": str(e), "status_code": 500}), 500