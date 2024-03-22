from rest_framework import serializers
from .models import Route, Bus, Trip
from django.db import models



class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

    def validate_name(self, value):
        if self.instance and self.instance.name == value:
            return value
        if Route.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Route with this name already exists.")
        return value

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'

    def validate_base_name(self, value):
        if self.instance and self.instance.base_name == value:
            return value
        if Bus.objects.filter(base_name__iexact=value).exists():
            raise serializers.ValidationError("Bus with this name already exists.")
        return value

class TripSerializer(serializers.ModelSerializer):
    remaining_seats = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = '__all__'

    def get_remaining_seats(self, obj):
        booked_seats = Trip.objects.filter(bus=obj.bus).count()
        remaining_seats = obj.bus.number_of_seats - booked_seats
        return remaining_seats


    def validate(self, data):
        if self.instance:
            # Check if the bus is already assigned to another trip
            existing_trip = Trip.objects.exclude(pk=self.instance.pk).filter(bus=data['bus']).filter(
                models.Q(departure_time__range=(data['departure_time'], data['arrival_time'])) |
                models.Q(arrival_time__range=(data['departure_time'], data['arrival_time'])) |
                models.Q(departure_time__lte=data['departure_time'], arrival_time__gte=data['arrival_time'])
            )
            if existing_trip.exists():
                raise serializers.ValidationError("This bus is already assigned to another trip at the same time.")
        else:
            # Check if the bus is already assigned to another trip
            existing_trip = Trip.objects.filter(bus=data['bus']).filter(
                models.Q(departure_time__range=(data['departure_time'], data['arrival_time'])) |
                models.Q(arrival_time__range=(data['departure_time'], data['arrival_time'])) |
                models.Q(departure_time__lte=data['departure_time'], arrival_time__gte=data['arrival_time'])
            )
            if existing_trip.exists():
                raise serializers.ValidationError("This bus is already assigned to another trip at the same time.")
        return data
