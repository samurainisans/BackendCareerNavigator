from flask import jsonify, request
from marshmallow import ValidationError

from app import db
from app.api.user_routes import api_blueprint

from app.models.jobapplication import JobApplication
from app.schemas.jobapplicationschema import JobApplicationSchema


@api_blueprint.route('/jobapplications', methods=['GET'])
def get_job_applications():
    job_applications = JobApplication.query.all()
    return jsonify(JobApplicationSchema(many=True).dump(job_applications)), 200


@api_blueprint.route('/jobapplications', methods=['POST'])
def add_job_application():
    job_application_data = request.json
    job_application = JobApplicationSchema().load(job_application_data)
    db.session.add(job_application)
    db.session.commit()
    return jsonify(JobApplicationSchema().dump(job_application)), 201


@api_blueprint.route('/jobapplications/<int:application_id>', methods=['PUT'])
def update_job_application(application_id):
    try:
        application_data = request.json
        application = JobApplication.query.get(application_id)
        if not application:
            return jsonify({"error": "JobApplication not found", "status_code": 404}), 404
        application = JobApplicationSchema().load(application_data, instance=application, partial=True)
        db.session.commit()
        return jsonify({"result": JobApplicationSchema().dump(application), "status_code": 200}), 200
    except ValidationError as ve:
        return jsonify({"error": str(ve), "status_code": 400}), 400
    except Exception as e:
        return jsonify({"error": str(e), "status_code": 500}), 500
