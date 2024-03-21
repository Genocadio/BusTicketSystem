from django.core.validators import MinLengthValidator, RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, user_type='normal'):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, user_type=user_type)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(email, name, password, user_type='admin')
        user.is_admin = True
        user.save(using=self._db)
        return user


def validate_password(value):
    validators = [
        MinLengthValidator(8, message='Password must be at least 8 characters long'),
        RegexValidator(regex=r'[A-Za-z]', message='Password must contain at least one letter'),
        RegexValidator(regex=r'[0-9]', message='Password must contain at least one digit')
    ]
    errors = {}
    for validator in validators:
        try:
            validator(value)
        except ValidationError as e:
            errors.update(e.message_dict)
    if errors:
        raise ValidationError(errors)


class User(AbstractBaseUser):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('normal', 'Normal'),
    ]

    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='normal')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()
