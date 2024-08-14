from django.urls import path
from .views import *

urlpatterns = [
    path("", AllWorkoutsView.as_view(), name="all workouts"),
    path("<int:workout_id>/", WorkoutView.as_view(), name="a workout"),
]