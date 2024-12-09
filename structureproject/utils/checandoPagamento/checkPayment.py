import mercadopago
from decouple import config


class PaymentCheck:
    def __init__(self, paymentid: str):
        self.sdk = mercadopago.SDK(config('ChaveSdkMercadoPagoProd')) 
        self.payment_id = paymentid    
    def _check_Status_payment_(self):
        payment_info = self.sdk.payment().get(self.payment_id)
        if payment_info["status"] == 200:
            return payment_info["response"]
        return {}

