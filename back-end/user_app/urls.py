from django.urls import path
from .views import *

urlpatterns = [
    path("", UserInfo.as_view(), name="user info"),
    path("register/", Register.as_view(), name="register user"),
    path("login/", LogIn.as_view(), name="user login"),
    path("logout/", LogOut.as_view(), name='user logout'),
]
