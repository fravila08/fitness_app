from django.db import models
from user_app.models import AppUser
from django.core import validators as v

# Create your models here.
class Workout(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='workouts')

class Exercise(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises')

class Set(models.Model):
    num_of_reps = models.PositiveIntegerField(
        null=False,
        blank=False,
        validators=[v.MinValueValidator(1), v.MaxValueValidator(200)]
    )
    weight = models.DecimalField(
        null=False,
        blank=False,
        max_digits=6, 
        decimal_places=2, 
        validators=[v.MinValueValidator(2.5), v.MaxValueValidator(1000.99)]
    )
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='sets')