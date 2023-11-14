from collections import OrderedDict
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app import db
from app.models.user import User
from app.schemas.userschema import UserSchema
from flask import g
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

        # Проверка наличия пользователя в базе данных
        user = User.query.filter_by(email=email, password=password).first()
        if not user:
            return jsonify({"error": "Invalid credentials", "status_code": 401}), 401

        # Создаем токен
        access_token = create_token(user.user_id, user.role)

        return jsonify({"access_token": access_token, "status_code": 200}), 200
    except Exception as e:
        return jsonify({"error": str(e), "status_code": 500}), 500

@api_blueprint.route('/register', methods=['POST'])
def register():
    try:
        user_data = request.json

        # Проверка на уникальность пользователя
        if User.query.filter_by(email=user_data.get('email')).first():
            return jsonify({"error": "User with this email already exists", "status_code": 400}), 400

        # Если пользователя с таким email нет, добавляем его в базу данных
        user = UserSchema().load(user_data)
        db.session.add(user)
        db.session.commit()

        # Создаем токен
        access_token = create_token(user.user_id, user.role)

        response = {
            "access_token": access_token,
            "status_code": 201,
            "message": "Registration successful"
        }
        return jsonify(response), 201
    except ValidationError as ve:
        return jsonify({"error": str(ve), "status_code": 400}), 400
    except Exception as e:
        return jsonify({"error": str(e), "status_code": 500}), 500

# Добавим защиту маршрута, требующую валидный токен
@api_blueprint.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@api_blueprint.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        if not users:
            return jsonify({"error": "No users found", "status_code": 404}), 404
        return jsonify({"result": UserSchema(many=True).dump(users), "status_code": 200}), 200
    except Exception as e:
        return jsonify({"error": str(e), "status_code": 500}), 500


@api_blueprint.route('/users', methods=['POST'])
def add_user():
    try:
        user_data = request.json

        # Проверка на уникальность пользователя
        if User.query.filter_by(email=user_data.get('email')).first():
            return jsonify({"error": "User with this email already exists", "status_code": 400}), 400

        # Если пользователя с таким email нет, добавляем его в базу данных
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
