from django.db import models
from buses.models import Trip
from users.models import User as CustomUser

class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    num_tickets = models.PositiveIntegerField(default=1)
    booking_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update available seats in the trip's bus
        self.trip.bus.number_of_seats -= self.num_tickets
        self.trip.bus.save()
