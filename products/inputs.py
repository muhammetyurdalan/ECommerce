import graphene


class CreateProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    category = graphene.Int(required=True)
    price = graphene.Int()
    image_url = graphene.String()
    description = graphene.String()
    date = graphene.Date()
    weight = graphene.Int()  
    
class UpdateProductInput(CreateProductInput):
    name = graphene.String()
    is_active = graphene.Boolean()
    is_done = graphene.Boolean()
    
    
class CreateCategoryInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    
    
class CreateVariationInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    

class CreateVariationOptionInput(graphene.InputObjectType):
    value = graphene.String(required=True)
    variation_id = graphene.Int(required=True)
    
class UpdateVariationOptionInput(CreateVariationOptionInput):
    value = graphene.String()
    variation_id = graphene.Int()
    
    
class CreateProductVariationInput(graphene.InputObjectType):
    product_id = graphene.Int(required=True)
    variation_option_id = graphene.Int(required=True)
    stock = graphene.Int()
    price = graphene.Decimal()
    
class UpdateProductVariationInput(CreateProductVariationInput):
    product_id = graphene.Int()
    variation_option_id = graphene.Int()


class CreateOrderItemInput(graphene.InputObjectType):
    product_variation_id = graphene.Int(required=True)
    quantity = graphene.Int(required=True)
    total_price = graphene.Decimal(required=True)


class CreateOrderInput(graphene.InputObjectType):
    total_price = graphene.Decimal(required=True)
    address = graphene.String(required=True)
    city_id = graphene.Int(required=True)
    order_items = graphene.List(CreateOrderItemInput, required=True)
    card_holder_name = graphene.String(required=True)
    card_number = graphene.String(required=True)
    expire_year = graphene.String(required=True)
    expire_month = graphene.String(required=True)
    cvv = graphene.String(required=True)
