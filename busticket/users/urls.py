from django.urls import path
from . import views

urlpatterns = [
    path('register', views.Register.as_view(), name='register'),
    path('login', views.loginView.as_view(), name='login'),
    path('user', views.UserView.as_view(), name='user'),
    path('logout', views.logoutView.as_view(), name='logout'),
    # path('logout/', views.logout, name='logout'),
    # path('register/', views.register, name='register'),
]