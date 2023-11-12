import os
from dotenv import load_dotenv
from flask import Flask
from app.extensions import db, ma

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ma.init_app(app)

    # from app.api.user_routes import api_blueprint
    # from app.api.city_routes import api_blueprint
    # from app.api.company_routes import api_blueprint
    # from app.api.job_routes import api_blueprint
    # from app.api.jobapplication_routes import api_blueprint
    # from app.api.employment_routes import api_blueprint
    # from app.api.worktype_routes import api_blueprint
    # from app.api.industry_routes import api_blueprint
    # app.register_blueprint(api_blueprint, url_prefix='/api')

    # with app.app_context():
        # db.create_all()
        # # Генерация данных для City
        # for _ in range(10):  # Пример для 10 городов
        #     city = City(title=fake.city())
        #     db.session.add(city)
        #
        # # Генерация данных для User
        # for _ in range(50):  # Пример для 50 пользователей
        #     user = User(username=fake.user_name(), email=fake.email(), password=fake.password(), role='user')
        #     db.session.add(user)
        #
        # # Генерация данных для Company
        # for _ in range(10):  # Пример для 10 компаний
        #     company = Company(name=fake.company(), industry_id=fake.random_int(min=1, max=3), description=fake.text(),
        #                       logo_url=fake.image_url())
        #     db.session.add(company)
        #
        # # Генерация данных для Job
        # for _ in range(50):  # Пример для 50 вакансий
        #     job = Job(title=fake.job(), description=fake.text(), salary=fake.random_int(min=10000, max=100000),
        #               experience=fake.job(), company_id=fake.random_int(min=1, max=10),
        #               type_id=fake.random_int(min=1, max=3),
        #               city_id=fake.random_int(min=1, max=10), employment_id=fake.random_int(min=1, max=3))
        #     db.session.add(job)
        #
        # # Генерация данных для JobApplication
        # job_application_statuses = ["Принято", "Отклонено", "На рассмотрении"]
        # for _ in range(50):  # Пример для 50 заявок
        #     jobapplication = JobApplication(
        #         user_id=fake.random_int(min=1, max=50),
        #         job_id=fake.random_int(min=1, max=50),
        #         status=fake.random_element(job_application_statuses)  # Случайный выбор статуса
        #     )
        #     db.session.add(jobapplication)
        #
        # # Генерация данных для Employment
        # for _ in range(3):  # Пример для 3 типов занятости
        #     employment = Employment(title=fake.job())
        #     db.session.add(employment)
        #
        # # Генерация данных для WorkType
        # for _ in range(3):  # Пример для 3 типов работы
        #     worktype = WorkType(title=fake.job())
        #     db.session.add(worktype)
        #
        # # Генерация данных для Industry
        # for _ in range(3):  # Пример для 3 отраслей
        #     industry = Industry(title=fake.job())
        #     db.session.add(industry)
        #
        # db.session.commit()

    return app

