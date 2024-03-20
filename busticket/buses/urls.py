from django.urls import path
from .views import RouteList, BusList

urlpatterns = [
    path('routes/', RouteList.as_view(), name='route-list'),
    path('buses/', BusList.as_view(), name='bus-list'),
    # Add more URL patterns as needed
]
