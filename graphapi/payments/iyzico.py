from graphapi.payments.base import IPayment
import iyzipay
import json
from django.conf import settings

api_key = "sandbox-9Uv7ud3hsB05Rq48klVnG7c1m9cn0v0u"
secret_key = "sandbox-nNeib27PlbU9rzcecYLEgSdjOoW7HSxv"


class Iyzico(IPayment):
    """
    Iyzico payment processing class.
    """

    def __init__(self, customer, order):
        self.headers = {
            'api_key': api_key,
            'secret_key': secret_key,
            'base_url': iyzipay.base_url
        }
        self.customer = customer
        self.order = order
        self.payment_data = None
        self.response = None

    def get_basket_items(self):
        items = self.order.items.all()
        basket_items = []
        for item in items:
            product = item.product_variation.product
            price = item.total_price * item.quantity
            basket_items.append({
                "id": item.id,
                "price": str(price),
                "name": f"Product #{product.id}",
                "category1": product.category.name,
                "itemType": "PHYSICAL"
            })
        return basket_items

    def initialize_payment(self, data):
        buyer = {
            "id": self.customer.id,
            "name": self.customer.first_name,
            "surname": self.customer.last_name,
            "identityNumber": self.customer.id_number,
            "email": self.customer.email,
            "gsmNumber": self.customer.phone,
            "registrationAddress": self.customer.address,
            "city": self.customer.city.name,
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
            "address": self.order.address,
            "contactName": self.customer.first_name + " " + self.customer.last_name,
            "city": self.order.city.name,
            "country": "Turkey"
        }
        payment_data = {
            "locale": "tr",
            "price": str(self.order.total_price),
            "paidPrice": str(self.order.total_price),
            "installment": 1,
            "basketId": str(self.order.id),
            "paymentChannel": "WEB",
            "paymentGroup": "PRODUCT",
            "conversationId": "ecommerce",
            "paymentCard": card,
            "buyer": buyer,
            "shippingAddress": address,
            "billingAddress": address,
            "basketItems": self.get_basket_items(),
            "currency": "TRY",
            "callbackUrl": settings.BACKEND_URL + '/process_payment_return/'
        }
        self.payment_data = payment_data

    def process_payment(self, data) -> bool:
        self.initialize_payment(data)
        payment = iyzipay.Payment()
        response = payment.create(self.payment_data, self.headers)
        response = json.load(response)
        self.response = response
        return True
    
    def cancel_payment(self) -> bool:
        if self.order.payment_id == '':
            return False
        request = {
        "locale": "tr",
        'conversationId': 'ecommerce',
        'paymentId': self.order.payment_id,
        }
        cancel = iyzipay.Cancel()
        response = cancel.create(request, self.headers)
        response = json.load(response)
        self.response = response
        return True

    def refund_payment(self, payment_id: str, amount: float) -> bool:
        # Implementation for refunding payment with Iyzico
        pass

    def is_success(self) -> bool:
        if self.response:
            return self.response.get('status', '') == 'success'
        return False
    
    def get_response(self) -> dict:
        if not self.response:
            return None
        return {
            'status': self.response.get('status', '') == 'success',
            'order_id': self.response.get('paymentId', ''),
            'error_code': self.response.get('errorCode', ''),
            'error_message': self.response.get('errorMessage', ''),
            'locale': self.response.get('locale', ''),
            'conversation_id': self.response.get('conversationId', ''),
            'basket_id': self.response.get('basketId', ''),
        }