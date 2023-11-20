from datetime import datetime
from sqlite3 import IntegrityError

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app import db
from app.api.user_routes import api_blueprint
from app.models.city import City
from app.models.company import Company
from app.models.employment import Employment

from app.models.job import Job
from app.models.jobapplication import JobApplication
from app.models.resume import Resume
from app.models.worktype import WorkType
from app.schemas.jobschema import JobSchema
from app.schemas.resumeschema import ResumeSchema


def create_response(data, status_code=200):
    return jsonify({"result": data, "status_code": status_code}), status_code


@api_blueprint.route('/jobs', methods=['GET'])
@jwt_required()
def get_jobs():
    try:
        current_user = get_jwt_identity()
        user_id = current_user['user_id']

        applied_job_ids = [job_application.job_id for job_application in
                           JobApplication.query.filter_by(resume_id=user_id)]

        print('applied_job_ids', applied_job_ids)

        jobs = Job.query.filter(~Job.job_id.in_(applied_job_ids)).all()

        print('jobs', jobs)

        return create_response(JobSchema(many=True).dump(jobs), 200)
    except Exception as e:
        return jsonify({"error": str(e), "status_code": 500}), 500


@api_blueprint.route('/jobs/hr', methods=['GET'])
@jwt_required()
def get_jobs_by_hr_id():
    try:
        current_user = get_jwt_identity()
        user_id = current_user['user_id']

        # Получаем компанию пользователя
        company = Company.query.filter_by(hr_id=user_id).first()

        if not company:
            return jsonify({"error": "User is not associated with any company", "status_code": 400}), 400

        # Получаем все вакансии связанные с компанией
        jobs = Job.query.filter_by(company_id=company.company_id).all()

        return create_response(JobSchema(many=True).dump(jobs), 200)
    except Exception as e:
        return jsonify({"error": str(e), "status_code": 500}), 500

@api_blueprint.route('/jobs', methods=['POST'])
@jwt_required()
def add_job():
    try:
        current_user = get_jwt_identity()
        user_id = current_user['user_id']

        job_data = request.json

        # Получение id города по его названию
        city = City.query.filter_by(title=job_data['city']).first()
        if not city:
            return create_response({"error": "City not found"}, 404)

        employment = Employment.query.filter_by(title=job_data['employment']).first()
        if not employment:
            return create_response({"error": "Employment not found"}, 404)

        # Получение id типа работы по его названию
        work_type = WorkType.query.filter_by(title=job_data['type']).first()
        if not work_type:
            return create_response({"error": "WorkType not found"}, 404)

        # Получение company_id по hr_id пользователя из токена
        company = Company.query.filter_by(hr_id=user_id).first()
        if not company:
            return create_response({"error": "User is not associated with any company"}, 400)

        # Создание нового объекта Job
        new_job = Job(
            company_id=company.company_id,
            type_id=work_type.type_id,
            city_id=city.city_id,
            employment_id=employment.employment_id,  # Проверьте, где вы получаете employment_id из запроса
            title=job_data['title'],
            description=job_data['description'],
            requirements="123",
            salary=job_data['salary'],
            experience=job_data['experience'],
            date_posted=datetime.utcnow()  # или используйте job_data['date_posted'], если он передается
        )

        db.session.add(new_job)
        db.session.commit()

        return jsonify({"msg": "Job added successfully", "status_code": 201}), 201
    except IntegrityError as ie:
        db.session.rollback()
        return create_response({"error": str(ie)}, 400)
    except ValidationError as ve:
        return create_response({"error": str(ve)}, 400)
    except Exception as e:
        print(e)
        return create_response({"error": str(e)}, 500)


@api_blueprint.route('/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    try:
        job_data = request.json
        job = Job.query.get(job_id)
        if not job:
            return create_response({"error": "Job not found"}, 404)

        if 'date_posted' in job_data and job_data['date_posted']:
            job_data['date_posted'] = datetime.fromisoformat(job_data['date_posted'])

        if 'work_type' in job_data:
            work_type_data = job_data.pop('work_type')
            work_type = WorkType.query.filter_by(type_id=work_type_data['type_id']).first()
            if work_type:
                job.type_id = work_type.type_id

        if 'city' in job_data:
            city_data = job_data.pop('city')
            city = City.query.filter_by(city_id=city_data['city_id']).first()
            if city:
                job.city_id = city.city_id

        if 'employment' in job_data:
            employment_data = job_data.pop('employment')
            employment = Employment.query.filter_by(employment_id=employment_data['employment_id']).first()
            if employment:
                job.employment_id = employment.employment_id

        if 'company' in job_data:
            company_data = job_data.pop('company')
            company = Company.query.filter_by(company_id=company_data['company_id']).first()
            if company:
                job.company_id = company.company_id

        for key, value in job_data.items():
            if hasattr(job, key):
                setattr(job, key, value)

        db.session.commit()

        return jsonify({"msg": "Job updated", "status_code": 200}), 200
    except IntegrityError as ie:
        db.session.rollback()
        return create_response({"error": str(ie)}, 400)
    except ValidationError as ve:
        return create_response({"error": str(ve)}, 400)
    except Exception as e:
        return create_response({"error": str(e)}, 500)
