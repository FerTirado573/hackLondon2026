from django.db import models
from django.utils import timezone
from datetime import timedelta

class StudySpace(models.Model):
    name = models.CharField(max_length=100)
    opening_hours = models.CharField(max_length=100)
    occupied = models.BooleanField(default=False)  # PIR motion
    last_motion_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    # Check if space is currently booked or occupied
    def is_available(self):
        now = timezone.now()
        active_booking = self.bookings.filter(active=True, start_time__lte=now, end_time__gte=now).first()
        return not self.occupied and active_booking is None

    def release_if_inactive(self):
        now = timezone.now()
        # auto-release PIR occupancy after 10 minutes of no motion
        if self.occupied and self.last_motion_at:
            if now - self.last_motion_at > timedelta(minutes=10):
                self.occupied = False
                self.save()

class Booking(models.Model):
    space = models.ForeignKey(StudySpace, related_name="bookings", on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.space.name} booking from {self.start_time} to {self.end_time}"