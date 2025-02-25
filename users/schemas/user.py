import graphene
from graphene_django.types import ObjectType
from graphql_jwt.mutations import JSONWebTokenMutation
from django.contrib.auth import get_user_model
from products.utils import decode_secret, send_verify_mail, set_attributes
from products.decorators import roles_required
from users.types import UserType
from users.inputs import CreateUserInput, UpdateUserInput

User = get_user_model()

class Query(ObjectType):
    user = graphene.Field(UserType,
                id=graphene.Int(required=True))
    users = graphene.List(UserType)
    
    @roles_required('MANAGER')
    def resolve_user(root, info, **kwargs):
        id = kwargs.get('id')
        return User.objects.get(pk=id)
        
    @roles_required('MANAGER')
    def resolve_users(root, info, **kwargs):
        return User.objects.all()


class CreateUser(graphene.Mutation):
    class Arguments:
        data = CreateUserInput(required=True)
    user = graphene.Field(UserType)
    
    @roles_required('MANAGER')
    def mutate(root, info, *args, **kwargs):
        data = kwargs.get('data')
        user = User()
        set_attributes(user, data)
        user.set_password(data.password)
        user.save()
        return CreateUser(user=user)
    

class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        data = UpdateUserInput(required=True)
    user = graphene.Field(UserType)
    
    @roles_required('MANAGER')
    def mutate(root, info, *args, **kwargs):
        id = kwargs.get('id')
        data = kwargs.get('data')
        user = User.objects.get(pk=id)
        set_attributes(user, data)
        if data.password is not None:
            user.set_password(data.password)
        user.save()
        return UpdateUser(user=user)
    

class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    user = graphene.Field(UserType)

    @roles_required('MANAGER')
    def mutate(root, info, **kwargs):
        id = kwargs.get('id')
        user = User.objects.get(pk=id)
        user.delete()
        return DeleteUser(user=None)
    

class GetToken(JSONWebTokenMutation):
    user = graphene.Field(UserType)
    
    @classmethod
    def resolve(cls, root, info, *args, **kwargs):
        return cls(user=info.context.user)
    

class VerifyUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        
    success = graphene.Boolean()
    
    #@roles_required('MANAGER')
    def mutate(self,info,**kwargs):
        username = kwargs.get('username')
        user = User.objects.get(username=username)
        send_verify_mail(user)
        return VerifyUser(success=True)


class ResetPassword(graphene.Mutation):
    class Arguments:
        secret = graphene.String(required=True)
        password = graphene.String(required=True)
        
    success = graphene.Boolean()
    
    #@roles_required('MANAGER')
    def mutate(self,info,**kwargs):
        password = kwargs.get('password')
        uuid = decode_secret(kwargs.get('secret'))
        try:
            user = User.objects.get(uuid=uuid)
        except User.DoesNotExist:
            return ResetPassword(success=False)
        user.set_password(password)
        user.save()
        return ResetPassword(success=True)
    
class Mutation(ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    get_token = GetToken.Field()
    verify_user = VerifyUser.Field()
    reset_password = ResetPassword.Field()
    
    
schema = graphene.Schema(query=Query, mutation=Mutation)

