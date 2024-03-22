from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Route, Bus, Trip
from .serializers import RouteSerializer, BusSerializer, TripSerializer
from users.permisions import IsAdminUser, IsNormalUser
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

class RouteDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class RouteList(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
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
    permission_classes = [IsAdminUser, IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
    def get(self, request):
        
        trips = Trip.objects.all()
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)

    def post(self, request):
        self.check_permissions(request)
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        serializer = TripSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        self.check_permissions(request)
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        trips = Trip.objects.all()
        trips.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
