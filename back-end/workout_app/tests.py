from django.test import TestCase, Client
from django.urls import reverse
from user_app.models import AppUser
from rest_framework.authtoken.models import Token
from .models import *
from .serializers import *
import json


# Create your tests here.
class WorkoutTests(TestCase):
    def setUp(self):
        self.user = AppUser.objects.create_user(
            **{
                "email": "fr4v1l4@gmail.com",
                "age": 26,
                "weight": 216.33,
                "height": 67,
                "username": "fravila08",
                "first_name": "Francisco",
                "last_name": "Avila",
                "password": "p3r553u5",
            }
        )
        token = Token.objects.create(user=self.user).key
        self.client = Client(headers={"Authorization": f"Token {token}"})
        self.workout_attributes = {"name": "Chest & Back", "user": self.user.id}

    def test_01_create_workout(self):
        try:
            self.workout_attributes["user"] = self.user
            new_workout = Workout(**self.workout_attributes)
            new_workout.full_clean()
            new_workout.save()
            self.assertIsInstance(new_workout, Workout)
        except Exception as e:
            print(e)
            self.fail()

    def test_02_serializer_creation(self):
        try:
            new_workout = WorkoutSerializer(data=self.workout_attributes, partial=True)
            if new_workout.is_valid():
                workout = new_workout.save()
                self.assertIsInstance(workout, Workout)
            else:
                raise Exception(new_workout.errors)
        except Exception as e:
            print(e)
            self.fail()

    def test_03_create_a_workout(self):
        try:
            response = self.client.post(
                reverse("all workouts"),
                data=self.workout_attributes,
                content_type="application/json",
            )
            with self.subTest():
                self.assertEqual(201, response.status_code)
            body = json.loads(response.content)
            self.assertEqual(
                body,
                {
                    "id": 3,
                    "exercises": [],
                    "name": self.workout_attributes.get("name"),
                    "user": self.user.id,
                },
            )
        except Exception as e:
            print(e)
            self.fail()

    def test_04_get_all_workouts(self):
        try:
            self.client.post(
                reverse("all workouts"),
                data=self.workout_attributes,
                content_type="application/json",
            )
            response = self.client.get(reverse("all workouts"))
            with self.subTest():
                self.assertEqual(response.status_code, 200)
            body = json.loads(response.content)
            self.assertEqual(
                body,
                [
                    x["name"]
                    for x in WorkoutSerializer(self.user.workouts.all(), many=True).data
                ],
            )
        except Exception as e:
            print(e)
            self.fail()

    def test_05_delete_a_workout(self):
        try:
            workout_id = json.loads(
                self.client.post(
                    reverse("all workouts"),
                    data=self.workout_attributes,
                    content_type="application/json",
                ).content
            ).get("id")
            response = self.client.delete(reverse("a workout", args=[workout_id]))
            with self.subTest():
                self.assertEqual(response.status_code, 200)
            body = json.loads(response.content)
            self.assertEqual(body, "Workout deleted")
        except Exception as e:
            print(e)
            self.fail()

    def test_06_get_a_workout(self):
        try:
            workout_id = json.loads(
                self.client.post(
                    reverse("all workouts"),
                    data=self.workout_attributes,
                    content_type="application/json",
                ).content
            ).get("id")
            response = self.client.get(reverse("a workout", args=[workout_id]))
            with self.subTest():
                self.assertEqual(response.status_code, 200)
            body = json.loads(response.content)
            self.assertEqual(
                body, WorkoutSerializer(self.user.workouts.get(id=workout_id)).data
            )
        except Exception as e:
            print(e)
            self.fail()

    def test_04_update_a_workout(self):
        try:
            workout_id = json.loads(
                self.client.post(
                    reverse("all workouts"),
                    data=self.workout_attributes,
                    content_type="application/json",
                ).content
            ).get("id")
            response = self.client.put(
                reverse("a workout", args=[workout_id]),
                data={"name": "Chest & tris"},
                content_type="application/json",
            )
            with self.subTest():
                self.assertEqual(response.status_code, 200)
            body = json.loads(response.content)
            self.assertEqual(
                body, WorkoutSerializer(self.user.workouts.get(id=workout_id)).data
            )
        except Exception as e:
            print(e)
            self.fail()
