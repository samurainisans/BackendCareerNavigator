from datetime import datetime

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app import db
from app.api.user_routes import api_blueprint
from app.models.job import Job

from app.models.jobapplication import JobApplication
from app.models.resume import Resume
from app.models.user import User
from app.schemas.jobapplicationschema import JobApplicationSchema


@api_blueprint.route('/jobapplications', methods=['GET'])
@jwt_required()
def get_job_applications():
    try:
        # Шаг 1: Получить идентификатор пользователя из токена
        current_user = get_jwt_identity()
        user_id = current_user['user_id']

        # Шаг 2: Фильтровать отклики по идентификатору пользователя
        job_applications = JobApplication.query \
            .join(Resume, JobApplication.resume_id == Resume.resume_id) \
            .filter(Resume.user_id == user_id) \
            .all()

        # Возвращать только отфильтрованные отклики
        return jsonify({"status_code": 200, "result": JobApplicationSchema(many=True).dump(job_applications)}), 200
    except Exception as e:
        return jsonify({"status_code": 500, "error": str(e)}), 500



@api_blueprint.route('/jobapplications', methods=['POST'])
@jwt_required()
def add_job_application():
    try:
        # Извлекаем параметры job_id и resume_id из строки запроса
        job_id = request.args.get('job_id')
        resume_id = request.args.get('resume_id')

        if not job_id or not resume_id:
            return jsonify({"msg": "Job ID and Resume ID are required", "status_code": 400}), 400

        # Проверка на существование сочетания resumeId и jobId
        existing_application = JobApplication.query.filter_by(job_id=job_id, resume_id=resume_id).first()

        if existing_application:
            return jsonify({"msg": "Resume has already been submitted for this job", "status_code": 406}), 406

        # Создание и сохранение новой заявки на работу
        job_application = JobApplication(job_id=job_id, resume_id=resume_id, status='На рассмотрении')
        db.session.add(job_application)
        db.session.commit()

        return jsonify({"msg": "Job application added successfully", "status_code": 201}), 201
    except Exception as e:
        return jsonify({"msg": str(e), "status_code": 500}), 500


@api_blueprint.route('/jobapplications/<int:application_id>', methods=['PUT'])
def update_job_application(application_id):
    try:
        application_data = request.json
        application = JobApplication.query.get(application_id)
        if not application:
            return jsonify({"msg": "JobApplication not found", "status_code": 404}), 404

        # Преобразование application_date из строки в datetime, если оно есть
        if 'application_date' in application_data and application_data['application_date']:
            application_data['application_date'] = datetime.fromisoformat(application_data['application_date'])

        # Обновление полей application
        for key, value in application_data.items():
            if hasattr(application, key):
                setattr(application, key, value)

        db.session.commit()

        return jsonify({"msg": "Job Application updated", "status_code": 200}), 200
    except ValidationError as ve:
        return jsonify({"msg": str(ve), "status_code": 400}), 400
    except Exception as e:
        return jsonify({"msg": str(e), "status_code": 500}), 500


@api_blueprint.route('/jobapplications/<int:application_id>', methods=['DELETE'])
def delete_job_application(application_id):
    try:
        application = JobApplication.query.filter_by(application_id=application_id).first()
        if not application:
            return jsonify({"msg": "Job application not found or not accessible", "status_code": 404}), 404

        db.session.delete(application)
        db.session.commit()

        return jsonify({"msg": "Job application deleted successfully", "status_code": 200}), 200
    except Exception as e:
        return jsonify({"msg": str(e), "status_code": 500}), 500
