import graphene

class CreateUserInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    email = graphene.String()
    
class UpdateUserInput(CreateUserInput):
    username = graphene.String()
    password = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()