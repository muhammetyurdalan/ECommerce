import random
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from products.filters import ProductFilter
from products.utils import set_attributes
from graphene import ObjectType
from products.models import Product
from products.types import ProductType
from products.inputs import CreateProductInput, UpdateProductInput
    
    
class Query(ObjectType):
    products_filter = DjangoFilterConnectionField(ProductType, 
                        filterset_class=ProductFilter)
    all_products = graphene.List(ProductType)
    products_done = graphene.List(ProductType)
    products_undone = graphene.List(ProductType)
    product = graphene.Field(ProductType, 
                        id=graphene.Int(required = True))
    random_product = graphene.Field(ProductType)
    
    def resolve_products_filter(self, info, **kwargs):
        return Product.objects.all()
    
    def resolve_all_products(self, info, **kwargs):
        return Product.objects.filter(is_active = True)
    
    def resolve_products_done(self, info, **kwargs):
        return Product.objects.filter(is_active = True,is_done = True)
    
    def resolve_products_undone(self, info, **kwargs):
        return Product.objects.filter(is_active = True,is_done = False)
    
    def resolve_product(self,info,**kwargs):
        id = kwargs.get('id')
        return Product.objects.get(pk=id)
    
    def resolve_random_product(self,info,**kwargs):
        products = Product.objects.filter(is_active = True)
        return products[random.randint(0,products.count())-1]
    
    
class CreateProduct(graphene.Mutation):
    class Arguments:
        data = CreateProductInput(required = True)
        
    product = graphene.Field(ProductType)
    
    def mutate(self,info,**kwargs):
        data = kwargs.get('data')
        product = Product()
        set_attributes(product, data)
        product.save()
        return CreateProduct(product=product)
    
class UpdateProduct(graphene.Mutation):
    class Arguments:
        data = UpdateProductInput()
        id = graphene.Int(required=True)
        
    product = graphene.Field(ProductType)
    
    def mutate(self,info,**kwargs):
        data = kwargs.get('data')
        id = kwargs.get('id')
        product = Product.objects.get(pk=id)
        set_attributes(product, data)               
        product.save()
        return UpdateProduct(product=product)
        
        
class DeleteProduct(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        
    product = graphene.Field(ProductType)
    
    def mutate(self,info,**kwargs):
        id = kwargs.get('id')
        product = Product.objects.get(pk=id)
        product.delete()
        return DeleteProduct(product=None)
    
class SelectProduct(graphene.Mutation):
    class Arguments:
        count = graphene.Int(required=True)
        
    products = graphene.List(ProductType)
    
    def mutate(self,info,**kwargs):
        count = kwargs.get('count')
        products = Product.objects.all()
        ids = [item.id for item in products]
        weights = [item.weight for item in products]
        selected_ids = random.choices(ids, weights=weights, k=count)
        products = Product.objects.filter(pk__in=selected_ids)
        return SelectProduct(products=products)
    
        
class Mutation(graphene.ObjectType):
  create_product = CreateProduct.Field()
  update_product = UpdateProduct.Field()
  delete_product = DeleteProduct.Field()
  select_product = SelectProduct.Field()
        
        
schema = graphene.Schema(query=Query, mutation=Mutation)