# Create your views here.
from django.shortcuts import get_object_or_404
from user_app.views import UserView
from rest_framework.response import Response
from rest_framework import status as s
from .serializers import *

class AllWorkoutsView(UserView):
    def get(self, request):
        user_workouts = request.user.workouts.all()
        return Response([x["name"] for x in WorkoutSerializer(user_workouts, many=True).data])
    
    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        new_workout = WorkoutSerializer(data=data, partial=True)
        if new_workout.is_valid():
            new_workout.save()
            return Response(new_workout.data, status=s.HTTP_201_CREATED)
        else:
            return Response(new_workout.errors, status=s.HTTP_400_BAD_REQUEST)
        
class WorkoutView(UserView):
    def get_workout(self, user, workout_id):
        return get_object_or_404(user.workouts, id=workout_id)
    
    def get(self, request, workout_id):
        workout = self.get_workout(request.user, workout_id)
        return Response(WorkoutSerializer(workout).data)
    
    def put(self, request, workout_id):
        workout = self.get_workout(request.user, workout_id)
        update_workout = WorkoutSerializer(workout, data=request.data, partial=True)
        if update_workout.is_valid():
            update_workout.save()
            return Response(update_workout.data)
        else:
            return Response(update_workout.errors, status=s.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, workout_id):
        workout = self.get_workout(request.user, workout_id)
        workout.delete()
        return Response("Workout deleted")