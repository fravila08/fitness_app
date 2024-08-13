from django.urls import path
from .views import *

urlpatterns = [
    path("register/", Register.as_view(), name="register user"),
    path("login/", LogIn.as_view(), name="log in"),
]
