from django.shortcuts import redirect
from django.conf import settings


def verify_user(request, user_id):
    return redirect(settings.FRONTEND + '/change-password/' + str(user_id) + '/')
