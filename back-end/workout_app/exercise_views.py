from rest_framework import status as s
from rest_framework.response import Response
from user_app.views import UserView
from .serializers import *
from django.shortcuts import get_object_or_404


class AllExercisesView(UserView):
    def get(self, request, workout_id):
        exercises = request.user.workouts.get(id=workout_id).exercises.all()
        return Response(ExerciseSerializer(exercises, many=True).data)

    def post(self, request, workout_id):
        data = request.data.copy()
        data["workout"] = workout_id
        exercise = ExerciseSerializer(data=data, partial=True)
        if exercise.is_valid():
            exercise.save()
            return Response(exercise.data, status=s.HTTP_201_CREATED)
        else:
            return Response(exercise.errors, status=s.HTTP_400_BAD_REQUEST)


class ExerciseView(UserView):
    def get_exercise(self, obj, exercise_id):
        return get_object_or_404(obj, id=exercise_id)

    def get(self, request, workout_id, exercise_id):
        exercise = self.get_exercise(
            request.user.workouts.get(id=workout_id).exercises, exercise_id
        )
        return Response(ExerciseSerializer(exercise).data)

    def put(self, request, workout_id, exercise_id):
        exercise = self.get_exercise(
            request.user.workouts.get(id=workout_id).exercises, exercise_id
        )
        updated_exercise = ExerciseSerializer(exercise, data=request.data, partial=True)
        if updated_exercise.is_valid():
            updated_exercise.save()
            return Response(updated_exercise.data)
        else:
            return Response(updated_exercise.errors, status=s.HTTP_400_BAD_REQUEST)

    def delete(self, request, workout_id, exercise_id):
        exercise = self.get_exercise(
            request.user.workouts.get(id=workout_id).exercises, exercise_id
        )
        exercise.delete()
        return Response("Exercise has been deleted")
