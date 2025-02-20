from django.urls import path
from graphene_django.views import GraphQLView
from graphene_file_upload.django import FileUploadGraphQLView
from django.views.decorators.csrf import csrf_exempt

from users.views import verify_user


urlpatterns = [
    path("graphql/", csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True))),
    path("verify_user/<int:user_id>/", verify_user),
]
