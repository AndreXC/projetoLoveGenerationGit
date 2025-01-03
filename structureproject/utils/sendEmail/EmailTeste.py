import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from django.conf import settings
from django.template.loader import render_to_string
from ...comuns.comuns import HostPagina

class EmailSender:
    def __init__(self):
        # Configurações do servidor SMTP
        self.server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        self.server.ehlo()
        self.server.starttls()
        self.server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        self.from_email = settings.EMAIL_HOST_USER

    def SendEmail(self, to_email, template_name, context, subject, fileQrcode):
        try:
            # Criação da mensagem
            html_message = render_to_string(template_name, context)
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.from_email
            msg["To"] = to_email
            msg.attach(MIMEText(html_message, "html"))

            # Adicionando o QR Code como anexo
            if fileQrcode:
                attachment = MIMEBase('application', 'octet-stream')
                attachment.set_payload(fileQrcode)  # Adicionando o conteúdo binário do QR Code
                encoders.encode_base64(attachment)
                attachment.add_header('Content-Disposition', 'attachment', filename="qrcode.png")
                msg.attach(attachment)

            # Enviar o e-mail
            self.server.sendmail(self.from_email, to_email, msg.as_string())

        finally:
            self.close()

    def send_emails(self, email, link, fileQrcode, idCompra):
            # Enviar e-mail para cliente
            self.SendEmail(
                to_email= email,
                template_name='LoveGenerationEmail.html',
                context={
                    'message': "Obrigado por confiar em nosso produto! Estamos enviando este e-mail com todos os detalhes para você. Temos certeza de que sua amada ou amado vai adorar essa surpresa especial.",
                    'link': link,
                    'IdCompra': idCompra,
                    'link_produtoView': HostPagina +'/produto/visualizar/'
                },
                subject="Sua Página de Amor foi criada com sucesso!",
                fileQrcode=fileQrcode  # Enviar o QR code como anexo
            )
        
    def close(self):
        self.server.quit()
