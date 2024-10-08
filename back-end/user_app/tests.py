from django.test import TestCase, Client
from django.urls import reverse
from .serializers import AppUser, UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
import json


# Create your tests here.
class UserTests(TestCase):
    def setUp(self):
        self.user_attributes = {
            "email": "fr4v1l4@gmail.com",
            "age": 26,
            "weight": 216.33,
            "height": 67,
            "username": "fravila08",
            "first_name": "Francisco",
            "last_name": "Avila",
            "password": "p3r553u5",
        }
        self.client = Client()

    def test_01_successful_user(self):
        try:
            new_user = AppUser.objects.create_user(**self.user_attributes)
            new_user.save()
            self.assertIsInstance(new_user, AppUser)
        except Exception as e:
            print(e)
            self.fail()

    def test_02_authenticating_user(self):
        try:
            user = authenticate(
                username=self.user_attributes.get("email"),
                password=self.user_attributes.get("password"),
            )
            self.assertEqual(user, AppUser.objects.first())
        except Exception as e:
            print(e)
            self.fail()

    def test_03_create_user_with_serializer(self):
        new_user = UserSerializer(data=self.user_attributes, partial=True)
        if new_user.is_valid():
            new_user.save()
            self.assertEqual(
                new_user.data, UserSerializer(AppUser.objects.first()).data
            )
        else:
            print(new_user.errors)
            self.fail()

    def test_04_register_user(self):
        try:
            response = self.client.post(
                reverse("register user"),
                data=self.user_attributes,
                content_type="application/json",
            )
            with self.subTest():
                self.assertEqual(response.status_code, 201)
            body = json.loads(response.content)
            user = AppUser.objects.first()
            test_body = {"user": user.username, "token": user.auth_token.key}
            self.assertEqual(body, test_body)
        except Exception as e:
            print(e)
            self.fail()

    def test_05_login_user(self):
        try:
            self.client.post(
                reverse("register user"),
                data=self.user_attributes,
                content_type="application/json",
            )
            response = self.client.post(
                reverse("user login"),
                data={
                    "email": self.user_attributes.get("email"),
                    "password": self.user_attributes.get("password"),
                },
                content_type="application/json",
            )
            with self.subTest():
                self.assertEqual(response.status_code, 200)
            body = json.loads(response.content)
            user = AppUser.objects.first()
            test_body = {"user": user.username, "token": user.auth_token.key}
            self.assertEqual(body, test_body)
        except Exception as e:
            print(e)
            self.fail()

    def test_06_user_logout(self):
        try:
            register_response = self.client.post(
                reverse("register user"),
                data=self.user_attributes,
                content_type="application/json",
            )
            token = json.loads(register_response.content).get("token")
            logout_response = self.client.post(
                reverse("user logout"), headers={"Authorization": f"Token {token}"}
            )
            with self.subTest():
                self.assertEqual(logout_response.status_code, 200)
            with self.subTest():
                self.assertFalse(Token.objects.all())
            content = json.loads(logout_response.content)
            self.assertEqual(content, "You have successfully logged out")
        except Exception as e:
            print(e)
            self.fail()

    def test_07_get_user_info(self):
        try:
            register_response = self.client.post(
                reverse("register user"),
                data=self.user_attributes,
                content_type="application/json",
            )
            token = json.loads(register_response.content).get("token")
            response = self.client.get(
                reverse("user info"), headers={"Authorization": f"Token {token}"}
            )
            with self.subTest():
                self.assertEqual(response.status_code, 200)
            content = json.loads(response.content)
            self.assertEqual(content, UserSerializer(AppUser.objects.first()).data)
        except Exception as e:
            print(e)
            self.fail()