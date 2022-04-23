from django.db import models
from django.utils import timezone
from user.models import CustomUser


class Message(models.Model):
    user_sender = models.OneToOneField(
        CustomUser, verbose_name=("user sender"), on_delete=models.CASCADE, related_name='message_sender')
    user_receiver = models.OneToOneField(
        CustomUser, verbose_name=("user receiver"), on_delete=models.CASCADE, related_name='message_receiver')
    message = models.CharField(max_length=250)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user_sender
