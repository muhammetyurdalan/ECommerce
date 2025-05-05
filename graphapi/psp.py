

from django.conf import settings
import json
import iyzipay


api_key = "sandbox-9Uv7ud3hsB05Rq48klVnG7c1m9cn0v0u"
secret_key = "sandbox-nNeib27PlbU9rzcecYLEgSdjOoW7HSxv"
base_url = "https://sandbox-api.iyzipay.com"

HEADERS = {
    'api_key': api_key,
    'secret_key': secret_key,
    'base_url': iyzipay.base_url
}


def get_basket_items(order):
    items = order.items.all()
    basket_items = []
    for item in items:
        product = item.product_variation.product
        price = item.total_price * item.quantity
        basket_items.append(
            {
                "id": item.id,
                "price": str(price),
                "name": f"Product #{product.id}",
                "category1": product.category.name,
                "itemType": "PHYSICAL"
            })
    return basket_items


def get_payment_data(data, customer, order):
    buyer = {
        "id": customer.id,
        "name": customer.first_name,
        "surname": customer.last_name,
        "identityNumber": customer.id_number,
        "email": customer.email,
        "gsmNumber": customer.phone,
        "registrationAddress": customer.address,
        "city": customer.city.name,
        "country": "Turkey",
    }
    card = {
        "cardHolderName": data.card_holder_name,
        "cardNumber": data.card_number,
        "expireYear": data.expire_year,
        "expireMonth": data.expire_month,
        "cvc": data.cvv,
    }
    address = {
        "address": order.address,
        "contactName": customer.first_name + " " + customer.last_name,
        "city": order.city.name,
        "country": "Turkey"
    }
    payment_data = {
        "locale": "tr",
        "price": str(order.total_price),
        "paidPrice": str(order.total_price),
        "installment": 1,
        "basketId": str(order.id),
        "paymentChannel": "WEB",
        "paymentGroup": "PRODUCT",
        "conversationId": "ottobus_transfer",
        "paymentCard": card,
        "buyer": buyer,
        "shippingAddress": address,
        "billingAddress": address,
        "basketItems": get_basket_items(order),
        "currency": "TRY",
        "callbackUrl": settings.BACKEND_URL + '/process_payment_return/'
    }
    return payment_data


def payment_process(data, customer, order):
    data = get_payment_data(data, customer, order)
    print(data)
    payment = iyzipay.Payment()
    response = payment.create(data, HEADERS)
    response = json.load(response)
    return response
