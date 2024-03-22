from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Route, Bus, Trip
from .serializers import RouteSerializer, BusSerializer, TripSerializer
from rest_framework import generics

class RouteDetail(generics.RetrieveDestroyAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class RouteList(APIView):
    def get(self, request):
        routes = Route.objects.all()
        serializer = RouteSerializer(routes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RouteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        routes = Route.objects.all()
        routes.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BusList(APIView):
    def get(self, request):
        buses = Bus.objects.all()
        serializer = BusSerializer(buses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        buses = Bus.objects.all()
        buses.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TripList(APIView):
    def get(self, request):
        trips = Trip.objects.all()
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TripSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        trips = Trip.objects.all()
        trips.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
