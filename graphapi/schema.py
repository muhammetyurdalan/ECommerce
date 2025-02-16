import graphene
from products import schema as products_schema
from users import schema as users_schema


class Query(
        products_schema.Query,
        users_schema.Query,
        graphene.ObjectType):
    pass


class Mutation(
        products_schema.Mutation,
        users_schema.Mutation,
        graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
