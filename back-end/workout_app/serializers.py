from .models import Workout, Exercise, Set
from rest_framework.serializers import ModelSerializer

class SetSerializer(ModelSerializer):
    class Meta:
        model = Set
        fields = '__all__'

class ExerciseSerializer(ModelSerializer):
    sets = SetSerializer(many=True)

    class Meta:
        model = Exercise
        fields = '__all__'

class WorkoutSerializer(ModelSerializer):
    exercises = ExerciseSerializer(many=True)

    class Meta:
        model = Workout
        fields = '__all__'