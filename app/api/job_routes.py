from flask import jsonify, request

from app import db
from app.api.user_routes import api_blueprint

from app.models.job import Job
from app.schemas.jobschema import JobSchema


@api_blueprint.route('/jobs', methods=['GET'])
def get_jobs():
    jobs = Job.query.all()
    return jsonify(JobSchema(many=True).dump(jobs))


@api_blueprint.route('/jobs', methods=['POST'])
def add_job():
    job_data = request.json
    job = JobSchema().load(job_data)
    db.session.add(job)
    db.session.commit()
    return jsonify(JobSchema().dump(job)), 201
