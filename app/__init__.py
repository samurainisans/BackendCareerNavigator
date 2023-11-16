import os
import random

from faker import Faker
from flask import Flask
from flask.cli import load_dotenv
from flask_jwt_extended import JWTManager

from app.extensions import db, ma
from app.models.city import City
from app.models.company import Company
from app.models.employment import Employment
from app.models.industry import Industry
from app.models.job import Job
from app.models.jobapplication import JobApplication
from app.models.resume import Resume
from app.models.user import User
from app.models.worktype import WorkType

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    db.init_app(app)
    ma.init_app(app)
    jwt = JWTManager(app)

    from app.api.user_routes import api_blueprint
    from app.api.city_routes import api_blueprint
    from app.api.company_routes import api_blueprint
    from app.api.job_routes import api_blueprint
    from app.api.jobapplication_routes import api_blueprint
    from app.api.employment_routes import api_blueprint
    from app.api.worktype_routes import api_blueprint
    from app.api.industry_routes import api_blueprint
    from app.api.resume_routes import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # fake = Faker('ru_RU')
    #
    # with app.app_context():
    #     db.create_all()
    #     for _ in range(5):
    #         city = City(title=fake.city())
    #         db.session.add(city)
    #
    #     for _ in range(10):
    #         user = User(first_name=fake.first_name(), last_name=fake.last_name(), phone_number=fake.phone_number(), email=fake.email(), password=fake.password(), role=random.choice(
    #             ['employer', 'user'])
    #         )
    #         db.session.add(user)
    #
    #     for _ in range(5):
    #         company = Company(name=fake.company(), industry_id=fake.random_int(min=1, max=3), description=fake.text(),
    #                           logo_url=fake.image_url())
    #         db.session.add(company)
    #
    #     for _ in range(10):
    #         job = Job(title=fake.job(), description=fake.text(), salary=fake.random_int(min=10000, max=100000),
    #                   experience=fake.job(), company_id=fake.random_int(min=1, max=10),
    #                   type_id=fake.random_int(min=1, max=3),
    #                   city_id=fake.random_int(min=1, max=10), employment_id=fake.random_int(min=1, max=3),
    #                   requirements=fake.text())
    #         db.session.add(job)
    #
    #     job_application_statuses = ["Принято", "Отклонено", "На рассмотрении"]
    #
    #     for _ in range(10):
    #         jobapplication = JobApplication(
    #             resume_id=fake.random_int(min=1, max=50),
    #             job_id=fake.random_int(min=1, max=50),
    #             status=fake.random_element(job_application_statuses)
    #         )
    #         db.session.add(jobapplication)
    #
    #     for _ in range(3):
    #         employment = Employment(title=fake.job())
    #         db.session.add(employment)
    #
    #     for _ in range(3):
    #         worktype = WorkType(title=fake.job())
    #         db.session.add(worktype)
    #
    #     for _ in range(3):
    #         industry = Industry(title=fake.job())
    #         db.session.add(industry)
    #
    #     for user_id in range(1, 16):
    #         resume = Resume(
    #             title=fake.job(),
    #             user_id=user_id,
    #             description=fake.text(max_nb_chars=500),
    #             experience=fake.text(max_nb_chars=100),
    #             education=fake.text(max_nb_chars=100),
    #             skills=fake.text(max_nb_chars=100),
    #             contact_info=fake.text(max_nb_chars=100),
    #         )
    #         db.session.add(resume)
    #
    #     db.session.commit()

    return app
