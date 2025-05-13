from . import iyzico
from django.conf import settings

class Providers:
    IYZICO = 'iyzico'
    PAYTR = 'paytr'
    PAYU = 'payu'


class PaymentServiceProvider:
    @staticmethod
    def get(order, customer=None):
        if settings.PSP == Providers.IYZICO:
            return iyzico.Iyzico(customer, order)
        # elif provider == Providers.PAYTR:
        #     return paytr.Paytr(customer, order)
        # elif provider == Providers.PAYU:
        #     return payu.Payu(customer, order)
        else:
            raise ValueError("Unsupported payment service provider")
