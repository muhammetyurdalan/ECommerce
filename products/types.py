import graphene
from graphene_django.types import DjangoObjectType
from graphene import relay
import products.models as models

class ProductType(DjangoObjectType):
    real_id = graphene.Int(source="id")
    name = graphene.String()
    price = graphene.Int()
    image_url = graphene.String()
    description = graphene.String()
    date = graphene.Date()
      
    class Meta:
        model = models.Product
        interfaces = (relay.Node,)
        
class CategoryType(DjangoObjectType):
    name = graphene.String()
      
    class Meta:
        model = models.Category
        
class VariationType(DjangoObjectType):
      
    class Meta:
        model = models.Variation
        
class VariationOptionType(DjangoObjectType):
      
    class Meta:
        model = models.VariationOption
        
class ProductVariationType(DjangoObjectType):
      
    class Meta:
        model = models.ProductVariation

class OrderType(DjangoObjectType):
    class Meta:
        model = models.Order

class OrderItemType(DjangoObjectType):
    class Meta:
        model = models.OrderItem
