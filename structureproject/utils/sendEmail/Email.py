from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from io import BytesIO
from ModelSite.models import  Error

class Sendemail:
    def __init__(self, recipient_email, subject, message, FileQrcode, link) -> None:
        self.recipient_email = 'lovegenerationcontato@outlook.com'
        self.subject = subject
        self.message = message
        self.file = FileQrcode
        self.link = link

    def send_email(self):
        try:
            # Renderiza o template HTML personalizado para o email
            html_content = render_to_string('LoveGenerationEmail.html', {
                'message': self.message,
                'link': self.link
            })

            # Cria o email com título, mensagem, e destinatário
            email = EmailMessage(
                subject=self.subject,
                body=html_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[self.recipient_email]
            )

            # Define o conteúdo do email como HTML
            email.content_subtype = 'html'

            # Anexa o arquivo PNG, binary para arquivo novamente!
            if self.file:
                qr_code_file = BytesIO(self.file)
                email.attach('qrcode.png', qr_code_file.getvalue(), 'image/png')

            # Envia o email
            email.send()
        except Exception as e:
            Error.objects.create(
            error_type=type(e).__name__,
            details='[SendEmail]'+ e)




