from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.serializers import UserSerializer
from django.utils import timezone
from users.models import User
from .permisions import IsAdminUser, IsNormalUser
from users.models import User, RefreshTokenEntry
from rest_framework import status

"""
* User view
* The raoutes here have three permissions
  * IsAdminUser
  * IsNormalUser
  * IsAuthenticated
* to pass all these permisions you must pass the token as authentication bearer token
  * the token must be valid and correspond to the required permissions
  * else the user wont be autorized
"""

class Register(APIView):
    """
     * route to register user
     * accepts json with email, name, password and user_type
     * user_type can be normal or admin 
     * if user_type is not provided, defaults to normal
     *"""
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    """
    * route to login user
    * accepts json with email and password
    * returns json with access_token and refresh_token
    """
    def post(self, request, format=None):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            raise AuthenticationFailed('Please provide both email and password')

        user = get_object_or_404(User, email=email)

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        # Delete any existing refresh token entry for the user
        RefreshTokenEntry.objects.filter(user=user).delete()

        # Generate access token and refresh token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Save refresh token to database
        refresh_token_entry = RefreshTokenEntry.objects.create(user=user, token=str(refresh))
        
        return Response({
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': str(refresh)
        })


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """ 
        * route to fetch user information
        * returns json with user information
        """
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


    def delete(self, request, email):
        """
        * route to delete user
        * accepts email address for the user
        * returns 204 No Content
        """
        self.check_permissions(request)  # Check if the user is authenticated
        self.permission_classes = [IsAdminUser]  # Set permission classes for admin user
        self.check_permissions(request)  # Check if the user has admin permissions

        user = get_object_or_404(User, email=email)  # Retrieve the user by email
        user.delete()  # Delete the user

        return Response({"message": f"User with email '{email}' has been deleted."}, status=status.HTTP_204_NO_CONTENT)


    def put(self, request):
        """
        * route to update user information
        * accepts json with email, name, password and user_type
        * user_type can be normal or admin
        * if user_type is not provided, defaults to normal
        * returns json with updated user information
        """
        self.check_permissions(request)
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        user = request.user
        serializer = UserSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        """
        * route for logging out user
        * returns  Logout successful
        """
        # Retrieve the user from the request object
        user = request.user
        
        try:
            # Retrieve the refresh token entry associated with the user
            refresh_token_entry = RefreshTokenEntry.objects.get(user=user)

            if refresh_token_entry:
                # Blacklist the refresh token
                refresh_token = RefreshToken(refresh_token_entry.token)
                refresh_token.blacklist()

                # Delete the refresh token entry from the database
                refresh_token_entry.delete()

            return Response({'message': 'Logout successful'})
        except RefreshTokenEntry.DoesNotExist:
            raise AuthenticationFailed('No refresh token found for the user')

class AdminView(APIView):
    """ 
    * route to fetch all users
    * returns json with user information for all registered users
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    