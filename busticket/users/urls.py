from django.urls import path
from . import views

urlpatterns = [
    path('register', views.Register.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('user', views.UserView.as_view(), name='user'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('users', views.AdminView.as_view(), name='all_users'),
    path('user/<str:email>/', views.UserView.as_view(), name='delete_user'),
]