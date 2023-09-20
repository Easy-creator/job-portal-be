from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import response, status
from users.serializers import RegisterationPoint, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class AuthUserApiView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user

        serializer = RegisterationPoint(user)
        return response.Response({'user': serializer.data})

class RegisterApiView(GenericAPIView):
    authentication_classes = []
    serializers_class = RegisterationPoint

    def post(self, request):
        serializers = self.serializers_class(data=request.data)

        if serializers.is_valid():
            serializers.save()
            return response.Response(serializers.data, status = status.HTTP_201_CREATED )
        
 
        return response.Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST )
    
    def get_serializer_class(self):
        return RegisterationPoint

class LoginApiView(GenericAPIView):
    authentication_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(username = email, password = password)
        
        if user:
            serializer = self.serializer_class(user)
            return response.Response(serializer.data, status = status.HTTP_200_OK)
        
        return response.Response({"message": "Invalid Username or Password Please try again"}, status = status.HTTP_401_UNAUTHORIZED)
