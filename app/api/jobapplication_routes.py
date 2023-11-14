from datetime import datetime

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app import db
from app.api.user_routes import api_blueprint
from app.models.job import Job

from app.models.jobapplication import JobApplication
from app.models.user import User
from app.schemas.jobapplicationschema import JobApplicationSchema

@api_blueprint.route('/jobapplications', methods=['GET'])
@jwt_required()
def get_job_applications():
    try:
        current_user = get_jwt_identity()
        user_id = current_user['user_id']

        # Фильтруем отклики только для текущего пользователя
        job_applications = JobApplication.query.filter_by(user_id=user_id).all()

        return jsonify({"status_code": 200, "result": JobApplicationSchema(many=True).dump(job_applications)}), 200
    except Exception as e:
        return jsonify({"status_code": 500, "error": str(e)}), 500


@api_blueprint.route('/jobapplications', methods=['POST'])
@jwt_required()
def add_job_application():
    try:
        current_user = get_jwt_identity()
        user_id = current_user['user_id']

        job_id = request.args.get('jobId')  # Получаем jobId из query parameters
        if job_id is None:
            return jsonify({"status_code": 400, "msg": "JobId is required in query parameters"}), 400

        # Проверяем, что job_id является целым числом
        try:
            job_id = int(job_id)
        except ValueError:
            return jsonify({"status_code": 400, "msg": "JobId must be an integer"}), 400

        # Проверяем, что job с таким id существует
        job = Job.query.get(job_id)
        if not job:
            return jsonify({"status_code": 404, "msg": "Job not found"}), 404

        # Создаем новый объект JobApplication
        job_application_data = {
            'user_id': user_id,
            'job_id': job_id,
            'application_date': datetime.utcnow(),
            'status': 'на рассмотрении'
        }

        job_application = JobApplication(**job_application_data)
        db.session.add(job_application)
        db.session.commit()

        return jsonify({"status_code": 201, "msg": "Job application added successfully"}), 201
    except Exception as e:
        return jsonify({"status_code": 500, "msg": str(e)}), 500

@api_blueprint.route('/jobapplications/<int:application_id>', methods=['PUT'])
def update_job_application(application_id):
    try:
        application_data = request.json
        application = JobApplication.query.get(application_id)
        if not application:
            return jsonify({"status_code": 404, "error": "JobApplication not found"}), 404

        # Преобразование application_date из строки в datetime, если оно есть
        if 'application_date' in application_data and application_data['application_date']:
            application_data['application_date'] = datetime.fromisoformat(application_data['application_date'])

        # Обновление полей application
        for key, value in application_data.items():
            if hasattr(application, key):
                setattr(application, key, value)

        db.session.commit()

        return jsonify({"status_code": 200, "result": JobApplicationSchema().dump(application)}), 200
    except ValidationError as ve:
        return jsonify({"status_code": 400, "error": str(ve)}), 400
    except Exception as e:
        return jsonify({"status_code": 500, "error": str(e)}), 500
