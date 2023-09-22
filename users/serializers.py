from rest_framework import serializers
from users.models import User, JobPost
from rest_framework.exceptions import ValidationError

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, DjangoUnicodeDecodeError, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from users.utils import Util
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed


class NewPassword(serializers.Serializer):
    password = serializers.CharField(max_length=16, min_length=6, write_only=True)
    token = serializers.CharField(write_only=True)
    encode = serializers.CharField(write_only=True)

    class Meta:
        fields = ['password', 'token', 'encode']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            encode = attrs.get('encode')

            id = force_str(urlsafe_base64_decode(encode))
            user = User.objects.get(id = id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            
            user.set_password(password)
            user.save()
            return user
        # except DjangoUnicodeDecodeError:
        except Exception as e:
            return AuthenticationFailed('This link is invalid', 401)
        return super().validate(attrs)

class ResetPWD(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ['email']


class RegisterationPoint(serializers.ModelSerializer):
    password = serializers.CharField(max_length=120, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'cv',)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class EmployerPoint(serializers.ModelSerializer):
    password = serializers.CharField(max_length=120, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'company_name',)

    def create(self, validated_data):
        name = validated_data["company_name"]
        if User.objects.filter(company_name = name).exists():
            raise ValidationError({"company_name": ["A user with this company name already exists."]})
        else:
            print('does not exist')
            return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=120, min_length=6, write_only=True)

    class Meta:
        model =User
        fields = ('email', 'password', 'token')
        read_only_fields = ['token']


class JobPostSerializer(serializers.ModelSerializer): # Job Post Serializer
    class Meta:
        model= JobPost
        fields="__all__"

