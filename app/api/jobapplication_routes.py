from flask import jsonify, request

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
    job_application_data = request.json
    job_application = JobApplication.query.get_or_404(application_id)
    # Проверка на принадлежность к компании (нужна дополнительная логика)
    job_application = JobApplicationSchema().load(job_application_data, instance=job_application)
    db.session.commit()
    return jsonify(JobApplicationSchema().dump(job_application))

