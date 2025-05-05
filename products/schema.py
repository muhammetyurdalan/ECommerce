import graphene
from .schemas.category import schema as category_schema
from .schemas.order import schema as order_schema
from .schemas.product_variation import schema as product_variation_schema
from .schemas.product import schema as product_schema
from .schemas.variation_option import schema as variation_option_schema
from .schemas.variation import schema as variation_schema


class Query(
        category_schema.Query,
        order_schema.Query,
        product_variation_schema.Query,
        product_schema.Query,
        variation_option_schema.Query,
        variation_schema.Query,
        graphene.ObjectType):
    pass


class Mutation(
        category_schema.Mutation,
        order_schema.Mutation,
        product_variation_schema.Mutation,
        product_schema.Mutation,
        variation_option_schema.Mutation,
        variation_schema.Mutation,
        graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
