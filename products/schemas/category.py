import graphene
from graphene import ObjectType
from products.models import Category
from products.types import CategoryType
from products.inputs import CreateCategoryInput

        
class Query(ObjectType):
    categories = graphene.List(CategoryType)
    category = graphene.Field(CategoryType, 
                        id=graphene.Int(required = True))
    
    def resolve_categories(self, info, **kwargs):
        return Category.objects.all()
    
    def resolve_category(self,info,**kwargs):
        id = kwargs.get('id')
        return Category.objects.get(pk=id)
    
    
class CreateCategory(graphene.Mutation):
    class Arguments:
        data = CreateCategoryInput(required = True)
        
    category = graphene.Field(CategoryType)
    
    def mutate(self,info,**kwargs):
        data = kwargs.get('data')
        category=Category(name=data.name)
        category.save()
        return CreateCategory(category=category)
    
class UpdateCategory(graphene.Mutation):
    class Arguments:
        data = CreateCategoryInput()
        id = graphene.Int(required = True)
        
    category = graphene.Field(CategoryType)
    
    def mutate(self,info,**kwargs):
        data = kwargs.get('data')
        id = kwargs.get('id')
        category=Category.objects.get(pk=id)
        if data.name is not None:
            category.name = data.name
        category.save()
        return UpdateCategory(category=category)
    
class DeleteCategory(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required = True)
        
    category = graphene.Field(CategoryType)
    
    def mutate(self,info,**kwargs):
        id = kwargs.get('id')
        category=Category.objects.get(pk=id)
        category.delete()
        return DeleteCategory(category=None)
        
        
        
class Mutation(graphene.ObjectType):
  create_category = CreateCategory.Field()
  update_category = UpdateCategory.Field()
  delete_category = DeleteCategory.Field()
        
        
schema = graphene.Schema(query=Query, mutation=Mutation)