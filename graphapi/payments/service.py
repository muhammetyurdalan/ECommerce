from . import iyzico
from django.conf import settings

class Providers:
    IYZICO = 'iyzico'
    PAYTR = 'paytr'
    PAYU = 'payu'


class PaymentServiceProvider:
    @staticmethod
    def get(*args, **kwargs):
        if settings.PAYMENT_PROVIDER == Providers.IYZICO:
            customer = kwargs.get('customer', None)
            order = kwargs.get('order', None)
            return iyzico.Iyzico(customer=customer, order=order)
        # elif provider == Providers.PAYTR:
        #     return paytr.Paytr(customer, order)
        # elif provider == Providers.PAYU:
        #     return payu.Payu(customer, order)
        else:
            raise ValueError("Unsupported payment service provider")



class PaymentService:
    def __init__(self, *args, **kwargs):
        self.provider = PaymentServiceProvider.get(*args, **kwargs)

    def process_payment(self, *args, **kwargs):
        self.provider.process_payment(*args, **kwargs)
        return self.provider

    def get_response(self, *args, **kwargs):
        self.provider.get_response(*args, **kwargs)
        return self.provider

    def is_success(self, *args, **kwargs):
        self.provider.is_success(*args, **kwargs)
        return self.provider

    def cancel_payment(self, *args, **kwargs):
        self.provider.cancel_payment(*args, **kwargs)
        return self.provider
