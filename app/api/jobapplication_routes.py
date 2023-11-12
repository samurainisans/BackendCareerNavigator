from datetime import datetime

from flask import jsonify, request
from marshmallow import ValidationError

from app import db
from app.api.user_routes import api_blueprint
from app.models.job import Job

from app.models.jobapplication import JobApplication
from app.models.user import User
from app.schemas.jobapplicationschema import JobApplicationSchema


@api_blueprint.route('/jobapplications', methods=['GET'])
def get_job_applications():
    try:
        job_applications = JobApplication.query.all()
        return jsonify({"status_code": 200, "result": JobApplicationSchema(many=True).dump(job_applications)}), 200
    except Exception as e:
        return jsonify({"status_code": 500, "error": str(e)}), 500

@api_blueprint.route('/jobapplications', methods=['POST'])
def add_job_application():
    try:
        job_application_data = request.json
        # Преобразование application_date из строки в datetime, если оно есть
        if 'application_date' in job_application_data and job_application_data['application_date']:
            job_application_data['application_date'] = datetime.fromisoformat(job_application_data['application_date'])


        # Обработка данных для job
        if 'job' in job_application_data:
            job_data = job_application_data.pop('job')
            job = Job.query.get(job_data.get('job_id'))
            if not job:
                return jsonify({"status_code": 404, "error": "Job not found"}), 404
            job_application_data['job_id'] = job.job_id

        # Обработка данных для user
        if 'user' in job_application_data:
            user_data = job_application_data.pop('user')
            user = User.query.get(user_data.get('user_id'))
            if not user:
                return jsonify({"status_code": 404, "error": "User not found"}), 404
            job_application_data['user_id'] = user.user_id

        # Создаем новый объект JobApplication
        job_application = JobApplication(**job_application_data)
        db.session.add(job_application)
        db.session.commit()

        return jsonify({"status_code": 201, "result": JobApplicationSchema().dump(job_application)}), 201
    except ValidationError as ve:
        return jsonify({"status_code": 400, "error": str(ve)}), 400
    except Exception as e:
        return jsonify({"status_code": 500, "error": str(e)}), 500

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
