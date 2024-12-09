from typing import Optional, List, Dict, Any


class PaymentData:
    def __init__(self, data: dict):
        self.transaction_id: Optional[str] = data.get("id")
        self.external_reference: Optional[str] = data.get("external_reference")
        self.payment_method: Optional[str] = (
            data.get("payment_method", {}).get("id")
        )
        
        self.name: Optional[str] = (
            data.get('point_of_interaction', {})
                .get('transaction_data', {})
                .get('bank_info', {})
                .get('collector', {})
                .get('account_holder_name')
        )

        self.description: Optional[str] = data.get("description")
        self.qr_code: Optional[str] = (
            data.get("point_of_interaction", {})
            .get("transaction_data", {})
            .get("qr_code")
        )
        self.qr_code_base64: Optional[str] = (
            data.get("point_of_interaction", {})
            .get("transaction_data", {})
            .get("qr_code_base64")
        )
        self.status: Optional[str] = data.get("status")
        self.ip_address: Optional[str] = (
            data.get("additional_info", {}).get("ip_address")
        )
        self.items: List[Dict[str, Any]] = data.get("additional_info", {}).get("items", [])

    @classmethod
    def from_json(cls, json_response: dict):
        """Método de classe para instanciar diretamente a partir de um JSON."""
        return cls(json_response)

    def __repr__(self):
        return (
            f"PaymentData(transaction_id={self.transaction_id}, "
            f"external_reference={self.external_reference}, "
            f"name={self.name}, "
            f"payment_method={self.payment_method}, "
            f"description={self.description}, "
            f"qr_code={self.qr_code}, "
            f"qr_code_base64={self.qr_code_base64}, "
            f"status={self.status}, "
            f"ip_address={self.ip_address}, "
            f"items={self.items})"
        )