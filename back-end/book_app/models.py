from django.db import models
from django.core import validators as v


# Create your models here.
class Book(models.Model):
    completed = models.BooleanField(default=False)
    current_page = models.PositiveIntegerField(
        default=1, validators=[v.MinValueValidator(1)]
    )
    last_read = models.DateTimeField(null=True, blank=True)
    title = models.CharField(blank=False, null=False)
    summary = models.TextField(null=True, blank=True)


class ReadingSummary(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="summaries")
    summary = models.TextField(blank=False, null=False)
    time_reading = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[v.MinValueValidator(0.07)],
        default=0.08,
    )
    pages_read = models.PositiveIntegerField(validators=[v.MinValueValidator(1)])
