from collections import OrderedDict
from flask import Blueprint, jsonify, request
from app import db
from app.models.user import User
from app.schemas.userschema import UserSchema

api_blueprint = Blueprint('api', __name__)

static_users = [
    {"user_id": 1, "username": "user1", "email": "user1@example.com", "role": "admin", "password_hash": "hash1"},
    {"user_id": 2, "username": "user2", "email": "user2@example.com", "role": "user", "password_hash": "hash2"},
]

@api_blueprint.route('/users', methods=['GET'])
def get_users():
    users_query = User.query.all()
    users_schema = UserSchema(many=True)
    users = users_schema.dump(static_users)

    response = OrderedDict([
        ('status_code', 200),
        ('result', users)
    ])

    return jsonify(response)


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
    user_data = request.json
    user = User.query.get_or_404(user_id)
    user = UserSchema().load(user_data, instance=user)
    db.session.commit()
    response = {
        "result": UserSchema().dump(user),
        "status_code": 200
    }
    return jsonify(response), 200
