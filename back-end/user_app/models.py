from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators as v


# Create your models here.
class AppUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    USERNAME_FIELD = "email"
    age = models.PositiveIntegerField(
        validators=[v.MinValueValidator(0), v.MaxValueValidator(120)]
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[v.MinValueValidator(0), v.MaxValueValidator(400)],
    )
    height = models.PositiveIntegerField(
        validators=[v.MinValueValidator(0), v.MaxValueValidator(96)]
    )
    REQUIRED_FIELDS = ["username", "age", "weight", "height"]
