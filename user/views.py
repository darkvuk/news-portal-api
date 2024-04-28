from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from .serializers import UserSerializer
from .models import User
from .mixins import UserPermissionMixin
import jwt
import datetime


class RegisterView(UserPermissionMixin, APIView):

    def post(self, request):
        if self.is_superuser(request):
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        
        return Response({'detail': 'You don\'t have access permission.'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class LoginView(APIView):

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found.')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorect password.')

        payload = {
            'id': user.user_id,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.now(datetime.timezone.utc)
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response


class UserView(APIView):
    
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(user_id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message": "Success."
        }
        return response
    

class UserList(UserPermissionMixin, APIView):

    def get(self, request):
        if self.is_superuser(request):
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        return Response(
            {'detail': 'You don\'t have access permission.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    

class UserDetail(UserPermissionMixin, APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        if self.is_owner(request, pk) or self.is_superuser(request):
            user = self.get_object(pk)
            serializer = UserSerializer(user, data=request.data)    # PATCH: add partial=True
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response(
            {'detail': 'User ID does not match the one in the token'},
            status=status.HTTP_401_UNAUTHORIZED
        )
        
    def delete(self, request, pk):
        if self.is_superuser(request):
            user_to_delete = self.get_object(pk)
            user_to_delete.delete()
            return Response(
                {'detail': 'User has been successfully deleted.'}, 
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {'detail': 'You don\'t have access permission.'},
            status=status.HTTP_401_UNAUTHORIZED
        )


    

