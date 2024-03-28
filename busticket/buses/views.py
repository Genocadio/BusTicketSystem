from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Route, Bus, Trip
from .serializers import RouteSerializer, BusSerializer, TripSerializer
from  users.permisions import IsAdminUser, IsNormalUser
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

"""
* Buses app Views, in this part we have three Authorisation classes
* IsAuthenticated: This class is used to check if the user is authenticated or not
* IsAdminUser: This class is used to check if the user is an admin or not
* IsNormalUser: This class is used to check if the user is a normal user or not
* To pass this authorisation permision you need to pass a valid token dedicated to apropriate user from Users app
* It is passed through Authentication header in the request 
"""
class RouteDetail(generics.RetrieveDestroyAPIView):
    """
    * Delete a single route from database
    * route id is required
    * admin token is required
    """
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class TripDetail(generics.RetrieveDestroyAPIView):
    """
    * Delete a trip from database
    * trip id is required
    * admin token is required
    """
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BusDetail(generics.RetrieveDestroyAPIView):
    """
    * Deletes a bus from database
    * bus id is required
    * admin token is required
    """
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RouteList(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    

    def get(self, request):
        """
        * route to fetch Routes information
        * returns json with Route information
        * requires autthentication 
        """
        try:
            routes = Route.objects.all()
            serializer = RouteSerializer(routes, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        * route to post Route information
        * requires route name and price for that journey to be provided
        * admin token is required
        * returns json with posted Route information 
        """
        try:
            serializer = RouteSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        """
        * deletes all routes
        * admin token is required
        * returns 204 no content on success 
        """
        try:
            routes = Route.objects.all()
            routes.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BusList(APIView):
    """
    *This class is for handling available buses, it  requires admin permision 
    """
    permission_classes = [IsAdminUser, IsAuthenticated]

    def get(self, request):
        """
        * this fetches all available buses
        * returns Json with Buses information  busa name, and number of seats as well as id
        """
        try:
            buses = Bus.objects.all()
            serializer = BusSerializer(buses, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        * Add buses by base_name and number of seats in Json
        * Returns added bus 
        """
        try:
            serializer = BusSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        """
        * Delete all buses from the database
        """
        try:
            buses = Bus.objects.all()
            buses.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TripList(APIView):
    """
    * Handles available trips
    * requires authentication token 
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        *fetch all trips available
        * requires authentication token
        """
        try:
            trips = Trip.objects.all()
            serializer = TripSerializer(trips, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """ 
        * Add A trip with a route id and bus id from database
        * add time in format  YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z] example 2024-03-30T10:30:00
        * deperture time and arrival time are required
        * admin token is required
        * a Two trips cant have same time
        """
        try:
            self.check_permissions(request)
            self.permission_classes = [IsAdminUser]
            self.check_permissions(request)
            serializer = TripSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        """ 
        * Delete all trips from the database
        * admin token is required
        """
        try:
            self.check_permissions(request)
            self.permission_classes = [IsAdminUser]
            self.check_permissions(request)
            trips = Trip.objects.all()
            trips.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
