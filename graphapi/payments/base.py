from abc import ABC, abstractmethod


class IPayment(ABC):
    """
    Interface for payment processing.
    """
    @abstractmethod
    def initialize_payment(self, data):
        """
        Initialize a payment with the given amount and currency.

        :param amount: The amount to be processed.
        :param currency: The currency of the payment.
        :return: A dictionary containing payment initialization details.
        """
        raise NotImplementedError("Subclasses should implement this method.")
    
    @abstractmethod
    def process_payment(self, data):
        """
        Process a payment of the given amount.

        :param amount: The amount to be processed.
        :return: True if the payment was successful, False otherwise.
        """
        raise NotImplementedError("Subclasses should implement this method.")
    
    @abstractmethod
    def cancel_payment(self, payment_id: str) -> bool:
        """
        Cancel a payment with the given payment ID.

        :param payment_id: The ID of the payment to be cancelled.
        :return: True if the cancellation was successful, False otherwise.
        """
        raise NotImplementedError("Subclasses should implement this method.")
    
    @abstractmethod
    def refund_payment(self, payment_id: str, amount: float) -> bool:
        """
        Refund a payment with the given payment ID.
        :param payment_id: The ID of the payment to be refunded.
        :param amount: The amount to be refunded.
        :return: True if the refund was successful, False otherwise.
        """
        raise NotImplementedError("Subclasses should implement this method.")
    
    @abstractmethod
    def is_success(self) -> bool:
        """
        Get the status of a payment with the given payment ID.
        :param payment_id: The ID of the payment to check.
        :return: A dictionary containing the payment status.
        """
        raise NotImplementedError("Subclasses should implement this method.")       