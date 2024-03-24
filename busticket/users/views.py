from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.serializers import UserSerializer
from django.utils import timezone
from users.models import User
from .permisions import IsAdminUser, IsNormalUser

class Register(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request, format=None):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            raise AuthenticationFailed('Please provide both email and password')

        user = get_object_or_404(User, email=email)

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        # Generate access token with expiry time
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Set access token as cookie
        response = Response()
        response.set_cookie(key='jwt', value=access_token, httponly=True)
        response.data = {
            'message': 'Login successful',
            'jwt': access_token,
        }
        return response

class UserView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    def delete(self, request):
        self.check_permissions(request)
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    def put(self, request):
        self.check_permissions(request)
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        user = request.user
        serializer = UserSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LogoutView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Successfully logged out'
        }
        return response

class AdminView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    
    def get(self, request):
        user_type = request.user.user_type
        return Response({"user type": user_type})

class NormalView(APIView):
    permission_classes = [IsNormalUser, IsAuthenticated]
    
    def get(self, request):
        user_type = request.user.user_type
        return Response({"user type": user_type})