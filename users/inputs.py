import graphene
from users.types import RoleChoices

class CreateUserInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    role = RoleChoices(required=True)
    phone = graphene.String()
    
class UpdateUserInput(CreateUserInput):
    username = graphene.String()
    password = graphene.String()
    name = graphene.String()
    email = graphene.String()
    role = RoleChoices()
    