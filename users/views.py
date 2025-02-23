from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.conf import settings


def verify_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_active = True
    user.save()
    return redirect(settings.FRONTEND + '/change-password/' + str(user_id) + '/')
