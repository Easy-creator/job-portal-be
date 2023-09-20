from rest_framework import serializers
from users.models import User
from rest_framework.exceptions import ValidationError


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