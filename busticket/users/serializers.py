from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'user_type']
        extra_kwargs = {
            'username': {'read_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user_type = validated_data.pop('user_type', 'normal')  # Default to 'normal' user type if not provided
        instance = self.Meta.model(**validated_data, user_type=user_type)
        if password is not None:
            instance.password = make_password(password)
        instance.save()
        return instance