"""Bus ticket booking system models for saving data to the database"""
from django.db import models


class Route(models.Model):
    """Route model for saving route information to the database"""
    name = models.CharField(max_length=100)


class Bus(models.Model):
    """Bus model for saving bus information to the database"""
    name = models.CharField(max_length=100)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    capacity = models.IntegerField()


class Place(models.Model):
    """Place model for saving place information to the database"""
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    number = models.IntegerField()
    is_reserved = models.BooleanField(default=False)