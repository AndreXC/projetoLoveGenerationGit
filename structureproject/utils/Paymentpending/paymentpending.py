from  ModelSite.models import Error
from ..sendEmail.EmailTeste import EmailSender

class PaymentPending:
    def __init__(self, email:str, qrcode:str, name:str, tokenReference: str):
            self.email:str = email
            self.qrcodepayload:str = qrcode
            self.name:str = name
            self.tokenReference:str =  tokenReference

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
             
        except Exception as e:
            Error.objects.create(
                error_type=type(e).__name__,
                details='[PaymentPending-SendEmail]'+ e)
