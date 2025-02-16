import graphene
from graphene import ObjectType
from products.utils import set_attributes
from products.models import Variation
from products.types import VariationType
from products.inputs import CreateVariationInput

Model = Variation
manager = Model.objects
Type = VariationType
CreateInput = CreateVariationInput
UpdateInput = CreateVariationInput

class Query(ObjectType):
    variation = graphene.Field(Type, id=graphene.Int(required=True))
    variations = graphene.List(Type)

    def resolve_variation(self, info, **kwargs):
        id = kwargs.get('id')
        return manager.get(pk=id)
    
    def resolve_variations(self, info, **kwargs):
        return manager.all()
    
    
class CreateVariation(graphene.Mutation):
    class Arguments:
        data = CreateInput(required=True)
    
    variation = graphene.Field(Type)
    
    def mutate(self, info, **kwargs):
        data = kwargs.get('data')
        instance = Model()
        set_attributes(instance, data)
        instance.save()
        return CreateVariation(variation=instance)
    
    
class UpdateVariation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        data = UpdateInput()
    
    variation = graphene.Field(Type)
    
    def mutate(self, info, **kwargs):
        id = kwargs.get('id')
        data = kwargs.get('data')
        instance = manager.get(pk=id)
        set_attributes(instance, data)
        instance.save()
        return UpdateVariation(variation=instance)
  
    
class DeleteVariation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    
    variation = graphene.Boolean()
    
    def mutate(self, info, **kwargs):
        id = kwargs.get('id')
        instance = manager.get(pk=id)
        instance.delete()
        return DeleteVariation(success=True)  


class Mutation(ObjectType):
    create_variation = CreateVariation.Field()
    update_variation = UpdateVariation.Field()
    delete_variation = DeleteVariation.Field()
    
schema = graphene.Schema(query=Query, mutation=Mutation)