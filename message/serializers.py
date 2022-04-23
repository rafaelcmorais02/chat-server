from ast import Mod
from dataclasses import fields
from pyexpat import model
from rest_framework.serializers import ModelSerializer
from .models import Message


class MessageSerializer(ModelSerializer):

    class Meta:
        model = Message
        fields = ['user_sender', 'user_receiver', 'message']
