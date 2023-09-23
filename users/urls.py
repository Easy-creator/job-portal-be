from .views import RegisterApiView, LoginApiView, AuthUserApiView, EmployerRegisterApiView, PasswordResetLink, PasswordTokenCheck, SetNewPassword, JobpostAPiview
from django.urls import path

app_name = 'users'

urlpatterns = [
    path('register/', RegisterApiView.as_view(), name="register"), #To register user
    path('login/', LoginApiView.as_view(), name="login"), #To login user
    path('user/', AuthUserApiView.as_view(), name="user"), # User Profile
    path('employer/', EmployerRegisterApiView.as_view(), name="employer"), # to register a new emoployer

    path('password/check_point/<token>/<encode>/', PasswordTokenCheck.as_view(), name="pwd_reset_check"), # Checking the token from the emial
    path('password/reset/', PasswordResetLink.as_view(), name="pwd_reset"),# sending confirmation email

    path('password/reset/set/', SetNewPassword.as_view(), name="pwd_reset_new"), # Set New Password

    path('jobpost/', JobpostAPiview.as_view(), name='job_post'), #Job Post URL
   

]
