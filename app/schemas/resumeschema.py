from marshmallow import fields

from app import ma
from app.models.resume import Resume
from app.models.user import User


class ResumeSchema(ma.SQLAlchemyAutoSchema):
    user = fields.Method("get_user")

    class Meta:
        model = Resume
        load_instance = True
        fields = (
            "title", "resume_id", "user", "experience", "education", "description", "skills",
            "contact_info")

    def get_user(self, obj):
        from app.schemas.userschema import UserSchema
        user = User.query.get(obj.user_id)
        return UserSchema().dump(user)
