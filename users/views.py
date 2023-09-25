from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import response, status
from users.serializers import RegisterationPoint, LoginSerializer, EmployerPoint, ResetPWD, NewPassword, JobPostSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from users.models import User, JobPost
from .paginations import LargeResultsSetPagination
from users.utils import Util
# Create your views here.

class PasswordResetLink(GenericAPIView):
    authentication_classes = []

    serializer_class = ResetPWD
    def post(self, request):
        data = {'request': request, 'data': request.data }
        serializer = self.serializer_class(data = data)
        # serializer.is_valid(raise_exception=True)
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            print(user)
            encode = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request).domain
            relative_link = reverse('users:pwd_reset_check', kwargs={'encode': encode, 'token': token})
            absurl = 'http://' + current_site + '/' + relative_link
            email_body = "Hi " + user.first_name + "Use the link below to verify your email \n" + absurl
            data = {'email_body': email_body, 'to_mail': user.email, 'email_subject': 'Verify your email'}

            Util.send_mail(data)
            return Response({'sucess': 'We have sent you an email'}, status=status.HTTP_200_OK)
        else: 
            return Response({'error': 'the email did not match any account'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

class PasswordTokenCheck(GenericAPIView):
    authentication_classes = []

    def get(self, request, token, encode):
        try:
            id = smart_str(urlsafe_base64_decode(encode))
            user = User.objects.get(id = id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid'}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'sucess': True, 'message': 'Valid link', 'token': token, 'encode': encode}, status=status.HTTP_200_OK)
            

        except DjangoUnicodeDecodeError:
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid'}, status=status.HTTP_400_BAD_REQUEST)
            
class SetNewPassword(GenericAPIView):
    authentication_classes = []

    serializer_class = NewPassword
    
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({'success': True, 'message': 'Password Sucessfully Changed'}, status=status.HTTP_202_ACCEPTED)


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

class EmployerRegisterApiView(GenericAPIView):
    authentication_classes = []
    serializers_class = EmployerPoint

    def post(self, request):
        name = request.data.get('company_name', None)
        

        serializers = self.serializers_class(data=request.data)

        if serializers.is_valid():
            serializers.save()
            return response.Response(serializers.data, status = status.HTTP_201_CREATED )
        

        return response.Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST )
    
    def get_serializer_class(self):
        return EmployerPoint

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

#Job post View
class JobpostAPiview(APIView): 
    authentication_classes = []
    serializer_class = JobPostSerializer

    def post(self, request):
        serializer= self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Job post done', 'data':serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg':'Unable to Job post', 'data':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        


class Jobpostfilter(APIView):
        def get(self, request):
            location = request.query_params.get('location')  
            
            if location:
                jobpost_queryset = JobPost.objects.filter(location=location)
                
                if jobpost_queryset.exists():  # Check if any job posts match the location
                    paginator= LargeResultsSetPagination()
                    page=paginator.paginate_queryset(jobpost_queryset, request)
                    print('page pagination', page)
                    serializer = JobPostSerializer(page, many=True)
                    return Response({'msg': 'Location wise data', 'data': serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response({'msg': 'No job post at this location'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'msg': 'Location parameter is missing'}, status=status.HTTP_400_BAD_REQUEST)
        
    
