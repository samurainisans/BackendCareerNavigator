from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app import db
from app.api.user_routes import api_blueprint
from app.models.resume import Resume
from app.models.user import User
from app.schemas.resumeschema import ResumeSchema


@api_blueprint.route('/resumes', methods=['POST'])
@jwt_required()
def add_resume():
    try:
        current_user = get_jwt_identity()
        user_id = current_user['user_id']

        user = User.query.get(user_id)
        if not user:
            return jsonify({"status_code": 404, "msg": "User not found"}), 404

        resume_data = request.json

        new_resume = Resume(
            user_id=user_id,
            description=resume_data.get('description', ''),
            experience=resume_data.get('experience', ''),
            education=resume_data.get('education', ''),
            skills=resume_data.get('skills', ''),
            contact_info=resume_data.get('contact_info', '')
        )

        db.session.add(new_resume)
        db.session.commit()

        return jsonify({"status_code": 201, "msg": "Resume added successfully"}), 201
    except Exception as e:
        return jsonify({"status_code": 500, "msg": str(e)}), 500


@api_blueprint.route('/resumes/<int:resume_id>', methods=['GET'])
def get_resume(resume_id):
    try:
        resume = Resume.query.get(resume_id)
        if not resume:
            return jsonify({"error": "Resume not found", "status_code": 404}), 404
        return jsonify({"result": ResumeSchema().dump(resume), "status_code": 200}), 200
    except Exception as e:
        return jsonify({"error": str(e), "status_code": 500}), 500


@api_blueprint.route('/resumes', methods=['GET'])
def get_all_resumes():
    try:
        resumes = Resume.query.all()
        if not resumes:
            return jsonify({"error": "No resumes found", "status_code": 404}), 404
        return jsonify({"result": ResumeSchema(many=True).dump(resumes), "status_code": 200}), 200
    except Exception as e:
        return jsonify({"error": str(e), "status_code": 500}), 500


@api_blueprint.route('/resumes/<int:resume_id>', methods=['PUT'])
def update_resume(resume_id):
    try:
        resume_data = request.json

        resume_data.pop('user', None)

        resume = Resume.query.get(resume_id)
        if not resume:
            return jsonify({"error": "Resume not found", "status_code": 404}), 404

        resume = ResumeSchema().load(resume_data, instance=resume, partial=True)
        db.session.commit()
        return jsonify({"msg": "Resume updated successfully", "status_code": 200}), 200
    except ValidationError as ve:
        return jsonify({"error": str(ve), "status_code": 400}), 400
    except Exception as e:
        return jsonify({"error": str(e), "status_code": 500}), 500


@api_blueprint.route('/resumes/<int:resume_id>', methods=['DELETE'])
def delete_resume(resume_id):
    try:
        resume = Resume.query.get(resume_id)
        if not resume:
            return jsonify({"error": "Resume not found", "status_code": 404}), 404
        db.session.delete(resume)
        db.session.commit()
        return jsonify({"msg": "Resume deleted successfully", "status_code": 200}), 200
    except Exception as e:
        return jsonify({"error": str(e), "status_code": 500}), 500
