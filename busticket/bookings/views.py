from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Booking
from .serializers import BookingSerializer
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated

class BookingList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        cached_bookings = cache.get('cached_bookings')
        if not cached_bookings:
            bookings = Booking.objects.all()
            serializer = BookingSerializer(bookings, many=True)
            cache.set('cached_bookings', serializer.data, timeout=60 * 15)  # Cache for 15 minutes
            return Response(serializer.data)
        return Response(cached_bookings)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Invalidate cached bookings after creating a new booking
            cache.delete('cached_bookings')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            booking_id = request.data.get('booking_id')  # Assuming booking_id is passed in the request data
            booking = Booking.objects.get(pk=booking_id)
            booking.delete()
            # Invalidate cached bookings after deleting a booking
            cache.delete('cached_bookings')
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Booking.DoesNotExist:
            return Response({"message": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
