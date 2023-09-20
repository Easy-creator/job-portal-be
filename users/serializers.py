from rest_framework import serializers
from users.models import User


class RegisterationPoint(serializers.ModelSerializer):
    password = serializers.CharField(max_length=120, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'cv',)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=120, min_length=6, write_only=True)

    class Meta:
        model =User
        fields = ('email', 'password', 'username', 'token')
        read_only_fields = ['token']