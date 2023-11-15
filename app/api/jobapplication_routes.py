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

        job_data = request.json.get('job')
        if not job_data:
            return jsonify({"msg": "Job data is required", "status_code": 400}), 400

        job_id = job_data.get('job_id')
        if job_id is None:
            return jsonify({"msg": "JobId is required in job data", "status_code": 400}), 400

        try:
            job_id = int(job_id)
        except ValueError:
            return jsonify({"msg": "JobId must be an integer", "status_code": 400}), 400

        job = Job.query.get(job_id)
        if not job:
            return jsonify({"msg": "Job not found", "status_code": 404}), 404

        job_application_data = {
            'user_id': user_id,
            'job_id': job_id,
            'application_date': datetime.utcnow(),
            'status': 'на рассмотрении'
        }

        job_application = JobApplication(**job_application_data)
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
