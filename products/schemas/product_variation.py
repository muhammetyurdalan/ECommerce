import graphene
from graphene import ObjectType
from products.utils import set_attributes
from products.models import ProductVariation
from products.types import ProductVariationType
from products.inputs import CreateProductVariationInput, UpdateProductVariationInput

Model = ProductVariation
manager = Model.objects
Type = ProductVariationType
CreateInput = CreateProductVariationInput
UpdateInput = UpdateProductVariationInput

class Query(ObjectType):
    product_variation = graphene.Field(Type, id=graphene.Int(required=True))
    product_variations = graphene.List(Type)
    
    def resolve_product_variation(self, info, **kwargs):
        id = kwargs.get('id')
        return manager.get(pk=id)
    
    def resolve_product_variations(self, info, **kwargs):
        return manager.all()


class CreateProductVariation(graphene.Mutation):
    class Arguments:
        data = CreateInput(required=True)
    
    product_variation = graphene.Field(Type)
    
    def mutate(self, info, **kwargs):
        data = kwargs.get('data')
        instance = Model()
        set_attributes(instance, data)
        instance.save()
        return CreateProductVariation(product_variation=instance)
    
    
class UpdateProductVariation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        data = UpdateInput()
    
    product_variation = graphene.Field(Type)
    
    def mutate(self, info, **kwargs):
        id = kwargs.get('id')
        data = kwargs.get('data')
        instance = manager.get(pk=id)
        set_attributes(instance, data)
        instance.save()
        return UpdateProductVariation(product_variation=instance)
  
    
class DeleteProductVariation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    
    success = graphene.Boolean()
    
    def mutate(self, info, **kwargs):
        id = kwargs.get('id')
        instance = manager.get(pk=id)
        instance.delete()
        return DeleteProductVariation(success=True)  


class Mutation(ObjectType):
    create_product_variation = CreateProductVariation.Field()
    update_product_variation = UpdateProductVariation.Field()
    delete_product_variation = DeleteProductVariation.Field()
    
schema = graphene.Schema(query=Query, mutation=Mutation)