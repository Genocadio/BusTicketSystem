from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Route, Bus, Place
from .serializers import RouteSerializer, BusSerializer, PlaceSerializer
from rest_framework.permissions import IsAuthenticated
from users.permisions import IsAdminUser, IsNormalUser

class RouteList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        routes = Route.objects.all()
        serializer = RouteSerializer(routes, many=True)
        return Response(serializer.data)

    def post(self, request):
        self.check_permissions(request)
        permission_classes = [IsAdminUser]
        for permission in permission_classes:
            if not permission().has_permission(request, self):
                return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = RouteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BusList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        buses = Bus.objects.all()
        serializer = BusSerializer(buses, many=True)
        return Response(serializer.data)

    def post(self, request):
        self.check_permissions(request)
        permission_classes = [IsAdminUser]
        for permission in permission_classes:
            if not permission().has_permission(request, self):
                return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = BusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
