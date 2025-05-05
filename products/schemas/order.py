import graphene
import graphapi.psp as psp
from graphene import ObjectType
from products.decorators import roles_required
from products.models import Order, OrderItem
from products.types import OrderType
from products.inputs import CreateOrderInput
from products.utils import set_attributes


class Query(ObjectType):
    orders = graphene.List(OrderType)
    order = graphene.Field(OrderType,
                           id=graphene.Int(required=True))

    def resolve_orders(self, info, **kwargs):
        return Order.objects.all()

    def resolve_order(self, info, **kwargs):
        id = kwargs.get('id')
        return Order.objects.get(pk=id)


class CreateOrder(graphene.Mutation):
    class Arguments:
        data = CreateOrderInput(required=True)

    order = graphene.Field(OrderType)

    @roles_required('CUSTOMER')
    def mutate(self, info, **kwargs):
        customer = info.context.user
        data = kwargs.get('data')
        order = Order.objects.create(
            user=customer, 
            address=data.address,
            city_id=data.city_id, 
            total_price=data.total_price
        )
        for item_data in data.order_items:
            order_item = OrderItem()
            set_attributes(order_item, item_data)
            order_item.order = order
            order_item.save()
            order_item.product_variation.stock -= item_data.quantity
            order_item.product_variation.save()
        response = psp.payment_process(data, customer, order)
        if response['status'] == 'success':
            order.status = 'PROCESSING'
            order.payment_id = response['paymentId']
            order.save()
        else:
            order.status = 'FAILED'
            order.save()
            for order_item in order.items.all():
                order_item.product_variation.stock -= order_item.quantity
                order_item.product_variation.save()
        return CreateOrder(order=order)


class Mutation(graphene.ObjectType):
    create_order = CreateOrder.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
