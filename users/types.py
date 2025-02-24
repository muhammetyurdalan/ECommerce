import graphene
from django.contrib.auth import get_user_model
from graphene_django.types import DjangoObjectType
import users.models as models

User = get_user_model()
RoleChoices = graphene.Enum.from_enum(models.Role)

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'role', 'name', 'email')