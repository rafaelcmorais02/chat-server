from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Message


class MessageSerializer(ModelSerializer):

    class Meta:
        model = Message
        fields = ['user_sender', 'user_receiver', 'message']

    def validate(self, data):
        if data['user_sender'] == data['user_receiver']:
            raise ValidationError(
                'Usuário rementente não pode ser igual ao usuário destinatário')
        return data
