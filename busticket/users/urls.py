from django.urls import path
from . import views

urlpatterns = [
    path('register', views.Register.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('user', views.UserView.as_view(), name='user'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('admin', views.AdminView.as_view(), name='admin'),
    path('normal', views.NormalView.as_view(), name='normal'),
    # path('login/', views.login, name='login'),
    # path('logout/', views.logout, name='logout'),
    # path('register/', views.register, name='register'),
]