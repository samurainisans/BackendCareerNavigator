# schemas/user_schema.py
from app import ma
from app.models.user import User
from marshmallow import fields


class UserSchema(ma.SQLAlchemyAutoSchema):
    password = fields.Str(load_only=True)

    class Meta:
        model = User
        load_instance = True
        # Указание, какие поля должны быть включены в сериализацию
        fields = ("user_id", "username", "email", "role", "password")
