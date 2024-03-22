from django.urls import path
from .views import RouteList, BusList, TripList, RouteDetail

urlpatterns = [
    path('routes/', RouteList.as_view(), name='route-list'),
    path('buses/', BusList.as_view(), name='bus-list'),
    path('trips/', TripList.as_view(), name='trip-list'),
    path('routes/<int:pk>/', RouteDetail.as_view()),
]
