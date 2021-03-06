from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class MyUserManager(BaseUserManager):
    def create_user(self, user_name, password=None, **extra_fields):
        """
        Creates and saves a User with the given user_name and password.
        """
        if not user_name:
            raise ValueError('Users must have an email address')

        user = self.model(
            user_name=self.normalize_email(user_name),
            **extra_fields
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, user_name, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            user_name=user_name,
            password=password,
            **extra_fields
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_name = models.EmailField(
        max_length=100, verbose_name='Nome do usuário', unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    password_confirmation = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    objects = MyUserManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.user_name


@receiver(post_save, sender=CustomUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
