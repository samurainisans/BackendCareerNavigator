from datetime import datetime
from sqlite3 import IntegrityError

from flask import jsonify, request
from marshmallow import ValidationError

from app import db
from app.api.user_routes import api_blueprint
from app.models.city import City
from app.models.company import Company
from app.models.employment import Employment

from app.models.job import Job
from app.models.worktype import WorkType
from app.schemas.jobschema import JobSchema
from app.schemas.worktypeschema import WorkTypeSchema

# Функция для оборачивания ответа в нужный формат
def create_response(data, status_code=200):
    return jsonify({"result": data, "status_code": status_code}), status_code


@api_blueprint.route('/jobs', methods=['GET'])
def get_jobs():
    jobs = Job.query.all()
    # Используем функцию для создания ответа
    return create_response(JobSchema(many=True).dump(jobs), 200)


@api_blueprint.route('/jobs', methods=['POST'])
def add_job():
    try:
        job_data = request.json
        # Преобразование date_posted из строки в datetime, если оно есть
        if 'date_posted' in job_data and job_data['date_posted']:
            job_data['date_posted'] = datetime.fromisoformat(job_data['date_posted'])

        # Проверяем и обрабатываем вложенные данные
        if 'work_type' in job_data:
            work_type_data = job_data.pop('work_type')
            work_type = WorkType.query.filter_by(type_id=work_type_data['type_id']).first()
            if not work_type:
                return create_response({"error": "WorkType not found"}, 404)
            job_data['type_id'] = work_type.type_id

        if 'city' in job_data:
            city_data = job_data.pop('city')
            city = City.query.filter_by(city_id=city_data['city_id']).first()
            if not city:
                return create_response({"error": "City not found"}, 404)
            job_data['city_id'] = city.city_id

        if 'employment' in job_data:
            employment_data = job_data.pop('employment')
            employment = Employment.query.filter_by(employment_id=employment_data['employment_id']).first()
            if not employment:
                return create_response({"error": "Employment not found"}, 404)
            job_data['employment_id'] = employment.employment_id

        if 'company' in job_data:
            company_data = job_data.pop('company')
            company = Company.query.filter_by(company_id=company_data['company_id']).first()
            if not company:
                return create_response({"error": "Company not found"}, 404)
            job_data['company_id'] = company.company_id

        # Создаем новый объект Job
        job = Job(**job_data)
        db.session.add(job)
        db.session.commit()

        return create_response(JobSchema().dump(job), 201)
    except IntegrityError as ie:
        db.session.rollback()
        return create_response({"error": str(ie)}, 400)
    except ValidationError as ve:
        return create_response({"error": str(ve)}, 400)
    except Exception as e:
        return create_response({"error": str(e)}, 500)


@api_blueprint.route('/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    try:
        job_data = request.json
        job = Job.query.get(job_id)
        if not job:
            return create_response({"error": "Job not found"}, 404)

        # Преобразование date_posted из строки в datetime, если оно есть
        if 'date_posted' in job_data and job_data['date_posted']:
            job_data['date_posted'] = datetime.fromisoformat(job_data['date_posted'])

        # Обновление данных job
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

        return create_response(JobSchema().dump(job), 200)
    except IntegrityError as ie:
        db.session.rollback()
        return create_response({"error": str(ie)}, 400)
    except ValidationError as ve:
        return create_response({"error": str(ve)}, 400)
    except Exception as e:
        return create_response({"error": str(e)}, 500)