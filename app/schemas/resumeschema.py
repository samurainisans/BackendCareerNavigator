from app import ma
from app.models.resume import Resume
from marshmallow import fields

from app.models.user import User


class ResumeSchema(ma.SQLAlchemyAutoSchema):
    user = fields.Method("get_user")

    class Meta:
        model = Resume
        load_instance = True
        fields = (
            "resume_id", "user", "summary", "experience", "education", "skills", "certifications", "personal_info",
            "contact_info")

    def get_user(self, obj):
        from app.schemas.userschema import UserSchema
        user = User.query.get(obj.user_id)
        return UserSchema().dump(user)
