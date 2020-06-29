from flask_app import ma
from flask_app.models import User


class RegisterSerializer(ma.Schema):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'active']
