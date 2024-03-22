from django.db import models

class Route(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Bus(models.Model):
    base_name = models.CharField(max_length=100, unique=True)
    number_of_seats = models.IntegerField()

    def __str__(self):
        return self.base_name

class Trip(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return f"Trip from {self.route.name} by {self.bus.base_name}"
