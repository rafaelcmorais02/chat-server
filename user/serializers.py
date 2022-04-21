from rest_framework.serializers import ModelSerializer, ValidationError
from .models import CustomUser


class UserRegisterSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('user_name', 'first_name',
                  'last_name', 'password', 'password_confirmation')

    def save(self):
        user = CustomUser(
            user_name=self.validated_data['user_name'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
        )
        password = self.validated_data['password']
        password_confirmation = self.validated_data['password_confirmation']
        if password != password_confirmation:
            raise ValidationError(
                {'password': 'As senhas devem ser iguais'})
        user.set_password(password)
