from flask import jsonify, request
from marshmallow import ValidationError

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


@api_blueprint.route('/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    try:
        job_data = request.json
        job = Job.query.get(job_id)
        if not job:
            return jsonify({"error": "Job not found", "status_code": 404}), 404
        job = JobSchema().load(job_data, instance=job, partial=True)
        db.session.commit()
        return jsonify({"result": JobSchema().dump(job), "status_code": 200}), 200
    except ValidationError as ve:
        return jsonify({"error": str(ve), "status_code": 400}), 400
    except Exception as e:
        return jsonify({"error": str(e), "status_code": 500}), 500
