from django.test import TestCase
from .serializers import AppUser, UserSerializer
from django.contrib.auth import authenticate


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
        }

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
        print(AppUser.objects.all())
        new_user = UserSerializer(data=self.user_attributes, partial=True)
        if new_user.is_valid():
            new_user.save()
            self.assertEqual(new_user.data, UserSerializer(AppUser.objects.first()).data)
        else:
            print(new_user.errors)
            self.fail()
            