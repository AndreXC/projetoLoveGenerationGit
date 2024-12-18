from  ModelSite.models import Error
from ..sendEmail.EmailTeste import EmailSender






class PaymentRejected:
    def __init__(self, Email:str,   tokenReference: str):
            self.email:str = Email
            self.tokenReference:str = tokenReference

    def __SendEmailRejected__(self):
        try:
            instanceSendEmail: EmailSender = EmailSender()
            instanceSendEmail.SendEmail(
                to_email=self.email,
                template_name='rejected.html',
                context={
                     'tokenReference': self.tokenReference
                },
                subject="Infelizmente seu Pagamento foi rejeitado!",
                fileQrcode=False
            )
             
            return True, ''
             
        except Exception as e:
            Error.objects.create(
                error_type=type(e).__name__,
                details='[SendEmailRejected-SendEmail]'+ e.args[0])
            return False, e.args[0]
