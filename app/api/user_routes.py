from collections import OrderedDict
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app import db
from app.models.user import User
from app.schemas.userschema import UserSchema

api_blueprint = Blueprint('api', __name__)


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
    user_data = request.json
    user = UserSchema().load(user_data)
    db.session.add(user)
    db.session.commit()
    response = {
        "result": UserSchema().dump(user),
        "status_code": 201
    }
    return jsonify(response), 201


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

