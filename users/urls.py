from .views import RegisterApiView, LoginApiView, AuthUserApiView
from django.urls import path

app_name = 'users'

urlpatterns = [
    path('register/', RegisterApiView.as_view(), name="register"), #To register user
    path('login/', LoginApiView.as_view(), name="login"), #To login user
    path('user/', AuthUserApiView.as_view(), name="user"), # testing authentication

]
