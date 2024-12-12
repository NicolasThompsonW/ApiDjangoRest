from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, min_length=5, required=True, allow_blank=False, allow_null=False)
    password = serializers.CharField(write_only=True, required=True, allow_blank=False, allow_null=False)
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already taken")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already taken")
        return value
    
class RegisterResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    date_joined = serializers.DateTimeField()
    

class PersonalDateViewSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    date_joined = serializers.DateTimeField()
    is_superuser = serializers.BooleanField()
    user_permissions = serializers.ListField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data


class RequestPasswordResetViewSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email does not exist")
        return value