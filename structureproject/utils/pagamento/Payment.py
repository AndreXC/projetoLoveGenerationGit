import mercadopago
import secrets
from decouple import config

class PaymentLinkGenerator:
    def __init__(self):
        # Inicializa o SDK do MercadoPago com a chave de autenticação
        self.sdk = mercadopago.SDK(config('ChaveSdkMercadoPagoProd'))
        self.secrete:str = secrets.token_hex(10) 
        self.Success: str= "http://127.0.0.1:8000/Aproved"
        self.failure:str ="https://meusite.com/falilure"
        self.pending:str = "https://meusite.com/Aproved"    

    def gerar_link_pagamento(self, items: dict[str, float, int]) -> dict[str, float, int]:
        payment_data = self._criar_dados_pagamento(items)
        result = self.sdk.preference().create(payment_data)
        if result['status'] == 201:
            return result["response"]
        return {}


    def _criar_dados_pagamento(self, items_list: dict[str, float, int]) -> dict[str, float, int]:
        return {
            "items": [items_list],
            "back_urls": {
                "success": self.Success,
                "failure": self.failure,
                "pending": self.pending,
            },
             "payment_methods": {
                "default_payment_method_id": "pix",
                "default_payment_type_id": "pix"
            },
            "external_reference": self.secrete,
            "auto_return": "approved" # retornar compras aprovadas automaticamente.
        }

