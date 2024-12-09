from  ModelSite.models import Error
from ..sendEmail.EmailTeste import EmailSender
import json
from ...dto.JsonGetProdutoFinal import TJSONGetProdutoFinal

class PaymentPending:
    def __init__(self, Email:str, qrcode:str, name:str, tokenReference: str):
            self.email:str = Email
            self.qrcodepayload:str = qrcode
            self.name:str = name
            self.tokenReference:str = tokenReference

    def __SendEmail__(self):
        try:
            instanceSendEmail: EmailSender = EmailSender()
            instanceSendEmail.__send_email(
                to_email=self.email,
                template_name='pending.html',
                context={
                     'name': self.name,
                     'qrcodePayload': self.qrcodepayload,
                     'tokenReference': self.tokenReference
                },
                subject="Lembrete, seu pagamento ainda não foi aprovado!",
            )
             
            return True, ''
             
        except Exception as e:
            Error.objects.create(
                error_type=type(e).__name__,
                details='[PaymentPending-SendEmail]'+ e.args[0])
            return False, e.args[0]
