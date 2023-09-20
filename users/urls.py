from .views import RegisterApiView, LoginApiView, AuthUserApiView, EmployerRegisterApiView
from django.urls import path

app_name = 'users'

urlpatterns = [
    path('register/', RegisterApiView.as_view(), name="register"), #To register user
    path('login/', LoginApiView.as_view(), name="login"), #To login user
    path('user/', AuthUserApiView.as_view(), name="user"),
    path('employer/', EmployerRegisterApiView.as_view(), name="employer"),


]
