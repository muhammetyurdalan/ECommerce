import graphene
from graphene_django.types import ObjectType
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from graphql_jwt.mutations import JSONWebTokenMutation
from django.contrib.auth.models import User
from products.utils import set_attributes
from products.decorators import roles_required
from users.types import UserType
from users.inputs import CreateUserInput, UpdateUserInput

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

def send_verify_mail(user):
    url = f"{settings.HOST}/verify_user/{user.id}/"
    subject = 'Verify Account'
    message = f'<p>Click on the link to verify your account</p><br><a href="{url}">Verify</a>'
    from_mail = settings.EMAIL_HOST_USER
    to_mail = [user.email]
    email = EmailMessage(subject, message, from_mail, to_mail)
    email.content_subtype = 'html'
    email.send()

class VerifyUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        
    success = graphene.Boolean()
    
    #@roles_required('MANAGER')
    def mutate(self,info,**kwargs):
        id = kwargs.get('id')
        user = User.objects.get(pk=id)
        send_verify_mail(user)
        return VerifyUser(success=True)

class Mutation(ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    get_token = GetToken.Field()
    verify_user = VerifyUser.Field()
    
    
schema = graphene.Schema(query=Query, mutation=Mutation)

