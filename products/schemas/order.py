import graphene
from graphapi.payments.psp import PaymentService
from graphene import ObjectType
from products.decorators import roles_required
from products.models import Order, OrderItem, ProductVariation
from products.types import OrderType
from products.inputs import AdminUpdateOrderInput, CreateOrderInput, UpdateOrderInput
from products.utils import set_attributes

manager= Order.objects
item_manager= OrderItem.objects
variation_manager= ProductVariation.objects


class Query(ObjectType):
    orders = graphene.List(OrderType)
    order = graphene.Field(OrderType,
                           id=graphene.Int(required=True))

    def resolve_orders(self, info, **kwargs):
        return Order.objects.all()

    def resolve_order(self, info, **kwargs):
        id = kwargs.get('id')
        return Order.objects.get(pk=id)


def decrease_stock(order):
    for order_item in order.items.all():
        product_variation = order_item.product_variation
        product_variation.stock -= order_item.quantity
        product_variation.save()


def increase_stock(order):
    for order_item in order.items.all():
        product_variation = order_item.product_variation
        product_variation.stock += order_item.quantity
        product_variation.save()


class CreateOrder(graphene.Mutation):
    class Arguments:
        data = CreateOrderInput(required=True)

    order = graphene.Field(OrderType)

    @roles_required('CUSTOMER')
    def mutate(self, info, **kwargs):
        customer = info.context.user
        data = kwargs.get('data')
        order_items = []
        order = Order.objects.create(
            user=customer, 
            address=data.address,
            city_id=data.city_id, 
            total_price=data.total_price
        )
        for item_data in data.order_items:
            order_item = OrderItem(order=order)
            set_attributes(order_item, item_data)
            order_items.append(order_item)
            variation = variation_manager.get(pk=item_data.product_variation_id)
            assert variation.stock >= item_data.quantity, "Not enough stock"
        item_manager.bulk_create(order_items)
        psp = PaymentService(customer=customer, order=order)
        response = psp.process_payment(data).get_response()
        if response['status'] == 'success':
            order.status = 'PROCESSING'
            order.payment_id = response['order_id']
            order.save()
            decrease_stock(order)
        else:
            order.status = 'FAILED'
            order.save()
        return CreateOrder(order=order)
    

class CancelOrder(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    order = graphene.Field(OrderType)

    @roles_required('CUSTOMER')
    def mutate(self, info, **kwargs):
        id = kwargs.get('id')
        order = Order.objects.get(pk=id)
        assert order.status == 'PROCESSING', "Order cannot be cancelled"
        response = psp.cancel_payment(order)
        assert response['status'] == 'success', "Payment cancellation failed"
        order.status = 'CANCELLED'
        order.save()
        increase_stock(order)
        return CancelOrder(order=order)
    

class UpdateOrder(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        data = UpdateOrderInput(required=True)

    order = graphene.Field(OrderType)

    @roles_required('CUSTOMER')
    def mutate(self, info, **kwargs):
        id = kwargs.get('id')
        data = kwargs.get('data')
        order = Order.objects.get(pk=id)
        assert order.status == 'PROCESSING', "Order cannot be updated"
        set_attributes(order, data)
        order.save()
        return UpdateOrder(order=order)


class AdminUpdateOrder(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        data = AdminUpdateOrderInput(required=True)

    order = graphene.Field(OrderType)

    @roles_required('ADMIN')
    def mutate(self, info, **kwargs):
        id = kwargs.get('id')
        data = kwargs.get('data')
        order = Order.objects.get(pk=id)
        set_attributes(order, data)
        order.save()
        return AdminUpdateOrder(order=order)


class Mutation(graphene.ObjectType):
    create_order = CreateOrder.Field()
    cancel_order = CancelOrder.Field()
    update_order = UpdateOrder.Field()
    admin_update_order = AdminUpdateOrder.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
