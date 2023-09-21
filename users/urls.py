from .views import RegisterApiView, LoginApiView, AuthUserApiView, EmployerRegisterApiView, PasswordResetLink, PasswordTokenCheck
from django.urls import path

app_name = 'users'

urlpatterns = [
    path('register/', RegisterApiView.as_view(), name="register"), #To register user
    path('login/', LoginApiView.as_view(), name="login"), #To login user
    path('user/', AuthUserApiView.as_view(), name="user"),
    path('employer/', EmployerRegisterApiView.as_view(), name="employer"),

    path('password/check_point/<token>/<encode>/', PasswordTokenCheck.as_view(), name="pwd_reset_check"),
    path('password/reset/', PasswordResetLink.as_view(), name="pwd_reset"),

]
