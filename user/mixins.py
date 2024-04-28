from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
import jwt

User = get_user_model()

class UserPermissionMixin:
    def is_logged_in(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        return User.objects.filter(user_id=payload['id']).first()
    
    def is_owner(self, request, pk):
        user = self.is_logged_in(request)
        return user.user_id == pk

    def is_superuser(self, request):
        user = self.is_logged_in(request)
        return user.is_superuser