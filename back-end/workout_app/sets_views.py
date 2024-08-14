from rest_framework import status as s
from rest_framework.response import Response
from user_app.views import UserView
from .serializers import *
from django.shortcuts import get_object_or_404


class AllSetsView(UserView):
    def get(self, request, workout_id, exercise_id):
        all_sets = (
            request.user.workouts.get(id=workout_id)
            .exercises.get(id=exercise_id)
            .sets.all()
        )
        return Response(SetSerializer(all_sets, many=True).data)

    def post(self, request, workout_id, exercise_id):
        exercise = request.user.workouts.get(id=workout_id).exercises.get(
            id=exercise_id
        )
        data = request.data.copy()
        data["exercise"] = exercise.id
        new_set = SetSerializer(data=data, partial=True)
        if new_set.is_valid():
            new_set.save()
            return Response(new_set.data, status=s.HTTP_201_CREATED)
        else:
            return Response(new_set.errors, status=s.HTTP_400_BAD_REQUEST)


class ASetView(UserView):
    def put(self, request, workout_id, exercise_id, set_id):
        a_set = get_object_or_404(
            request.user.workouts.get(id=workout_id).exercises.get(id=exercise_id).sets,
            id=set_id,
        )
        data = request.data.copy()
        updated_set = SetSerializer(a_set, data=data, partial=True)
        if updated_set.is_valid():
            updated_set.save()
            return Response(updated_set.data)
        else:
            return Response(updated_set.errors, status=s.HTTP_400_BAD_REQUEST)

    def delete(self, request, workout_id, exercise_id, set_id):
        a_set = get_object_or_404(
            request.user.workouts.get(id=workout_id).exercises.get(id=exercise_id).sets,
            id=set_id,
        )
        a_set.delete()
        return Response("Set ahs been deleted")
