# Marshmallow схемы для сериализации


from app import ma
from app.models.user import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        fields = ('user_id', 'username', 'email', 'role')



#к