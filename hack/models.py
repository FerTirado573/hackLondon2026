# spaces/models.py
from django.db import models

class StudySpace(models.Model):
    name = models.CharField(max_length=100)
    opening_hours = models.CharField(max_length=100, blank=True)  # e.g., "08:00-22:00"
    occupied = models.BooleanField(default=False)

    def __str__(self):
        return self.name