from datetime import datetime

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app import db
from app.models.city import City
from app.models.company import Company
from app.models.resume import Resume
from app.models.user import User
from app.schemas.userschema import UserSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_jwt_extended import JWTManager

api_blueprint = Blueprint('api', __name__)
jwt = JWTManager()


def create_token(user_id, role):
    access_token = create_access_token(identity={"user_id": user_id, "role": role})
    return access_token


@api_blueprint.route('/login', methods=['POST'])
def login():
    try:
        user_data = request.json
        email = user_data.get('email')
        password = user_data.get('password')

        user = User.query.filter_by(email=email, password=password).first()
        if not user:
            return jsonify(
                {"access_token": "", "msg": "Login or password incorrect", "status_code": 401, "role": ""}), 401

        if user.status == "denied":
            return jsonify(
                {"access_token": "", "msg": "Ваша регистрация была отклонена", "status_code": 403, "role": user.role})
        if user.status == "pending review":
            return jsonify(
                {"access_token": "", "msg": "Ваша регистрация еще не одобрена, попробуйте позже", "status_code": 403, "role": user.role})

        access_token = create_token(user.user_id, user.role)

        return jsonify(
            {"access_token": access_token, "msg": "Login successful", "status_code": 200, "role": user.role}), 200
    except Exception as e:
        return jsonify({"error": str(e), "status_code": 500}), 500


@api_blueprint.route('/pending_employers', methods=['GET'])
@jwt_required()
def get_pending_employers():
    try:
        # Получаем текущего пользователя
        current_user = get_jwt_identity()

        # Проверяем, является ли текущий пользователь администратором
        if current_user['role'] != 'admin':
            return jsonify({"error": "Access forbidden", "status_code": 403}), 403

        # Получаем всех пользователей с ролью "employer" и статусом "pending review"
        pending_employers = User.query.filter_by(role='employer', status='pending review').all()


        # Преобразуем данные в список словарей
        pending_employers_data = []
        for employer in pending_employers:
            company = Company.query.filter_by(hr_id=employer.user_id).first()
            print(company)
            employer_data = {
                "user_id": employer.user_id,
                "first_name": employer.first_name,
                "last_name": employer.last_name,
                "email": employer.email,
                "phone_number": employer.phone_number,
                "registration_date": employer.registration_date.strftime("%Y-%m-%d %H:%M:%S"),
                "company_name": company.name,
                "status": employer.status
            }
            pending_employers_data.append(employer_data)

        # Возвращаем данные о пользователях
        return jsonify({"pending_employers": pending_employers_data, "status_code": 200}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e), "status_code": 500}), 500

@api_blueprint.route('/register', methods=['POST'])
def register():
    try:
        user_data = request.get_json(force=True)

        print(user_data)

        # Проверка наличия пользователя с таким email
        if User.query.filter_by(email=user_data.get('email')).first():
            return jsonify(
                {"error": "User with this email already exists", "msg": "User already exists", "status_code": 400, }), 400

        status = ''
        if user_data.get('role') == 'user':
            status = 'accepted'
        if user_data.get('role') == 'employer':
            status = 'pending review'


        # Создание объекта NewUser из полученных данных
        new_user = User(
            first_name=user_data.get('firstName'),
            last_name=user_data.get('lastName'),
            email=user_data.get('email'),
            registration_date=datetime.utcnow(),
            phone_number=user_data.get('phone'),
            password=user_data.get('password'),
            role=user_data.get('role'),
            status=status
        )

        # Сохранение пользователя в базе данных
        db.session.add(new_user)
        db.session.commit()

        # Создание токена доступа
        access_token = create_token(new_user.user_id, new_user.role)

        # Формирование ответа
        response = {
            "access_token": access_token,
            "status_code": 201,
            "msg": "Registration successful",
            "role": new_user.role
        }
        return jsonify(response), 201

    except ValidationError as ve:
        return jsonify({"error": str(ve), "status_code": 400}), 400
    except Exception as e:
        print(e)
        return jsonify({"error": str(e), "status_code": 500}), 500


@api_blueprint.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

user_blueprint = Blueprint('user', __name__)


@api_blueprint.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    try:
        current_user = get_jwt_identity()
        user_id = current_user['user_id']

        # Получение пользователя из базы данных по его ID
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found", "status_code": 404}), 404

        # Получение резюме пользователя из базы данных
        resumes = Resume.query.filter_by(user_id=user.user_id).all()

        # Преобразование резюме в список словарей
        resumes_data = []
        for resume in resumes:
            city = City.query.filter_by(city_id=resume.city_id).first()
            resume_data = {
                "id": resume.resume_id,
                "title": resume.title,
                "description": resume.description,
                "experience": resume.experience,
                "education": resume.education,
                "skills": resume.skills,
                "contact_info": resume.contact_info,
                "age": resume.age,
                "citizenship": resume.citizenhip,
                "city": {
                    "title": city.title,
                    "city_id": city.city_id
                }
            }
            resumes_data.append(resume_data)

        # Возвращаем данные пользователя и его резюме
        user_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone_number": user.phone_number,
            "role": user.role,
            "email": user.email,
            "resumes": resumes_data
        }

        return jsonify({"user": user_data, "status_code": 200}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e), "status_code": 500}), 500


@api_blueprint.route('/users', methods=['POST'])
def add_user():
    try:
        user_data = request.json

        if User.query.filter_by(email=user_data.get('email')).first():
            return jsonify({"error": "User with this email already exists", "status_code": 400}), 400

        user = UserSchema().load(user_data)
        db.session.add(user)
        db.session.commit()
        response = {
            "result": UserSchema().dump(user),
            "status_code": 201
        }
        return jsonify(response), 201
    except ValidationError as ve:
        return jsonify({"error": str(ve), "status_code": 400}), 400
    except Exception as e:
        print(e)
        return jsonify({"error": str(e), "status_code": 500}), 500


@api_blueprint.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user_data = request.json
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found", "status_code": 404}), 404
        user = UserSchema().load(user_data, instance=user, partial=True)
        db.session.commit()
        return jsonify({"result": UserSchema().dump(user), "status_code": 200}), 200
    except ValidationError as ve:
        return jsonify({"error": str(ve), "status_code": 400}), 400
    except Exception as e:
        return jsonify({"error": str(e), "status_code": 500}), 500


@api_blueprint.route('/registration/<int:user_id>/reject', methods=['PATCH'])
def reject_registration_application(user_id):
    try:

        user = User.query.get(user_id)
        if not user:
            return jsonify({"msg": "user not found", "status_code": 404}), 404

        # Обновляем статус отклика на "Отклонено"
        user.status = 'accepted'
        db.session.commit()

        return jsonify({"msg": "Registration Application rejected", "status_code": 200}), 200
    except Exception as e:
        return jsonify({"msg": str(e), "status_code": 500}), 500


@api_blueprint.route('/registration/<int:user_id>/accept', methods=['PATCH'])
def accept_registration_application(user_id):
    try:

        user = User.query.get(user_id)
        if not user:
            return jsonify({"msg": "user not found", "status_code": 404}), 404

        # Обновляем статус отклика на "Отклонено"
        user.status = 'denied'
        db.session.commit()

        return jsonify({"msg": "Registration Application accepted", "status_code": 200}), 200
    except Exception as e:
        return jsonify({"msg": str(e), "status_code": 500}), 500