from django.urls import path
from .views import *
from .exercise_views import *
from .sets_views import *

urlpatterns = [
    path(
        "", 
        AllWorkoutsView.as_view(), 
        name="all workouts"
    ),
    path(
        "<int:workout_id>/", 
        WorkoutView.as_view(), 
        name="a workout"
    ),
    path(
        "<int:workout_id>/exercises/", 
        AllExercisesView.as_view(), 
        name="all exercises"
    ),
    path(
        "<int:workout_id>/exercises/<int:exercise_id>/",
        ExerciseView.as_view(),
        name="an exercise",
    ),
    path(
        "<int:workout_id>/exercises/<int:exercise_id>/sets/",
        AllSetsView.as_view(),
        name="all sets",
    ),
    path(
        "<int:workout_id>/exercises/<int:exercise_id>/sets/<int:set_id>/",
        ASetView.as_view(),
        name="a sets",
    ),
]
