import graphene
from graphene import ObjectType
from products.utils import set_attributes
from products.models import VariationOption
from products.types import VariationOptionType
from products.inputs import CreateVariationOptionInput, UpdateVariationOptionInput

Model = VariationOption
manager = Model.objects
Type = VariationOptionType
CreateInput = CreateVariationOptionInput
UpdateInput = UpdateVariationOptionInput

class Query(ObjectType):
    variation_option = graphene.Field(Type, id=graphene.Int(required=True))
    variation_options = graphene.List(Type)
    
    def resolve_variation_option(self, info, **kwargs):
        id = kwargs.get('id')
        return manager.get(pk=id)
    
    def resolve_variation_options(self, info, **kwargs):
        return manager.all()


class CreateVariationOption(graphene.Mutation):
    class Arguments:
        data = CreateInput(required=True)
    
    variation_option = graphene.Field(Type)
    
    def mutate(self, info, **kwargs):
        data = kwargs.get('data')
        instance = Model()
        set_attributes(instance, data)
        instance.save()
        return CreateVariationOption(variation_option=instance)
    
    
class UpdateVariationOption(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        data = UpdateInput()
    
    variation_option = graphene.Field(Type)
    
    def mutate(self, info, **kwargs):
        id = kwargs.get('id')
        data = kwargs.get('data')
        instance = manager.get(pk=id)
        set_attributes(instance, data)
        instance.save()
        return UpdateVariationOption(variation_option=instance)
  
    
class DeleteVariationOption(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    
    success = graphene.Boolean()
    
    def mutate(self, info, **kwargs):
        id = kwargs.get('id')
        instance = manager.get(pk=id)
        instance.delete()
        return DeleteVariationOption(success=True)  


class Mutation(ObjectType):
    create_variation_option = CreateVariationOption.Field()
    update_variation_option = UpdateVariationOption.Field()
    delete_variation_option = DeleteVariationOption.Field()
    
schema = graphene.Schema(query=Query, mutation=Mutation)