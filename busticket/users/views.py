from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.exceptions import AuthenticationFailed
from .models import User
import jwt, datetime
class Register(APIView):
     def post(self, request, format=None):
          serializer = UserSerializer(data=request.data)
          serializer.is_valid(raise_exception=True)
          serializer.save()
          return Response(serializer.data)

class loginView(APIView):
     def post(self, request, format=None):
          email = request.data['email']
          password = request.data['password']
          
          user = User.objects.filter(email=email).first()
          if user is None:
               raise AuthenticationFailed('Unregistered user')
          if user.check_password(password):
               payload = {
                    'id': user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                    'iat': datetime.datetime.utcnow()
               }
               token = jwt.encode(payload, 'secret', algorithm='HS256')
               response = Response()
               response.set_cookie(key='jwt', value=token, httponly=True)
               response.data = {
                    'jwt': token
               }
               return response
          else:
               raise AuthenticationFailed('Invalid password')

class UserView(APIView):
     def get(self, request):
          token = request.COOKIES.get('jwt')
          if token is not None:
               try:
                    payload = jwt.decode(token,'secret', algorithms=['HS256'])
               except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Token has expired')

               user = User.objects.get(id=payload['id'])
               serializer = UserSerializer(user)
               return Response(serializer.data)
          else:
               raise AuthenticationFailed('Unauthenticated')

class logoutView(APIView):
     def post(self, request):
          response = Response()
          response.delete_cookie('jwt')
          response.data = {
               'message': 'successfully logged out'
          }
          return response