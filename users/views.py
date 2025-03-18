from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import get_user_model
from products.utils import decode_secret

User = get_user_model()

def verify_user(request, secret):
    payload = decode_secret(secret)
    try:
        user = User.objects.get(uuid=payload.get('uuid'))
        user.is_verified = True
        user.save()
        return redirect(settings.FRONTEND_URL + '/verify_user_frontend/success/')
    except User.DoesNotExist:
        return redirect(settings.FRONTEND_URL + '/verify_user_frontend/failed/')
