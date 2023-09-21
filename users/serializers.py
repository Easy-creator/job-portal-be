from rest_framework import serializers
from users.models import User, JobPost
from rest_framework.exceptions import ValidationError

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, DjangoUnicodeDecodeError, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from users.utils import Util

class ResetPWD(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ['email']

    # def validate(self, attrs):
    #     try:
    #         email = attrs['data'].get('email', '')
    #         if User.objects.filter(email=email).exists():
    #             user = User.objects.get(email=email)
    #             encode = urlsafe_base64_encode(user.id)
    #             token = PasswordResetTokenGenerator().make_token(user)
    #             current_site = get_current_site(attrs['request']).domain
    #             relative_link = reverse('pwd_reset_check', kwargs={'encode': encode, 'token': token})
    #             absurl = 'http://' + current_site + '/' + relative_link
    #             email_body = "Hi " + user.first_name + "Use the link below to verify your email \n" + absurl
    #             data = {'email_body': email_body, 'to_mail': user.email, 'email_subject': 'Verify your email'}

    #             Util.send_mail(data)

            
    #         return attrs
        
    #     except:
    #         pass

    #     return super().validate(attrs)

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

