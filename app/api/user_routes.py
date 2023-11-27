from datetime import datetime

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app import db
from app.models.city import City
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
                {"error": "Invalid credentials", "msg": "Login or password incorrect", "status_code": 401}), 401

        access_token = create_token(user.user_id, user.role)

        return jsonify(
            {"access_token": access_token, "msg": "Login successful", "status_code": 200, "role": user.role}), 200
    except Exception as e:
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

        # Создание объекта NewUser из полученных данных
        new_user = User(
            first_name=user_data.get('firstName'),
            last_name=user_data.get('lastName'),
            email=user_data.get('email'),
            registration_date=datetime.utcnow(),
            phone_number=user_data.get('phone'),
            password=user_data.get('password'),
            role=user_data.get('role')
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
