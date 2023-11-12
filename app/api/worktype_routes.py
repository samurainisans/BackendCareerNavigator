from flask import jsonify

from app.api.user_routes import api_blueprint


from app.models.worktype import WorkType
from app.schemas.worktypeschema import WorkTypeSchema

@api_blueprint.route('/worktypes', methods=['GET'])
def get_worktypes():
    worktypes = WorkType.query.all()
    return jsonify(WorkTypeSchema(many=True).dump(worktypes))
