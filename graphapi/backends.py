from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from graphql_jwt.exceptions import JSONWebTokenError
from graphql_jwt.utils import get_credentials, get_payload
from graphql_jwt.settings import jwt_settings

User = get_user_model()
class AuthenticationBackend(ModelBackend):
    def authenticate(self, info, *args, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        if username is None or password is None:
            return None
        try:
            user = User.objects.get(username=username)
            if user is not None and not getattr(user, 'is_active',True):
                raise JSONWebTokenError('User is disabled')
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
    
class JSONWebTokenBackend():
    def authenticate(self, request=None, *args, **kwargs):
        if request is None  or getattr(request, '_jwt_token_auth', False):
            return None
        token = get_credentials(request, **kwargs)
        if token is None:
            return None
        payload = get_payload(token, request)
        username = jwt_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER(payload)
        if not username:
                raise JSONWebTokenError('Invalid token.')
        try:
            user = User.objects.get(username=username)
            if user is not None and not getattr(user, 'is_active',True):
                raise JSONWebTokenError('User is disabled')
            return user
        except User.DoesNotExist:
            return None
        