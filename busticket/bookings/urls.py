from django.urls import path
from .views import BookingList, BookingDel

urlpatterns = [
    path('bookings', BookingList.as_view(), name='booking-list'),
    path('booking/<int:booking_id>', BookingDel.as_view(), name='booking-delete'),
]
