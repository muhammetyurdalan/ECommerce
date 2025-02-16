from django.contrib.auth.models import User
from graphene_django.types import DjangoObjectType

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'profile')