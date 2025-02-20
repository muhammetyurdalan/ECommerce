from django.http import HttpResponse
from django.contrib.auth.models import User


def verify_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_active = True
    user.save()
    return HttpResponse('User verified successfully')
