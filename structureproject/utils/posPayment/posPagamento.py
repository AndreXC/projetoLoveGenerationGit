from ...dto.JsonGetProdutoFinal import TJSONGetProdutoFinal
from ModelSite.models import Compra, Qrcode
from ..Qrcode.createQrcode import QRCodeGenerator
from  ...comuns.comuns import HostPagina 
import secrets
from ..sendEmail.Email import Sendemail
from ..sendEmail.EmailTeste import EmailSender
import json
from django.db import close_old_connections





class createEstruturaProject:
    def __init__(self, ExternalReference: str):
        self.reference: str = ExternalReference 
        self.InstanceCompra: Compra = Compra.objects.get(token_referencia=self.reference)

        # Atribui um novo token a self.TokenLove se estiver vazio
        self.InstanceCompra.TokenLove = secrets.token_hex(64) if self.InstanceCompra.TokenLove == '' else self.InstanceCompra.TokenLove
        self.InstanceCompra.save()   

        self.link = f'{HostPagina}/Pagina/{self.reference}/{self.InstanceCompra.TokenLove}'       
    
    def __createQrcode__(self, StrErr: str) -> bool:
        try:
            StrErr = ''
            instanceQrcodeCreate: QRCodeGenerator = QRCodeGenerator()
            result, StrErr, qrcodeReturn = instanceQrcodeCreate.generate_qr_code(data=self.link)
            if not result and StrErr != '':
                return False, StrErr
            close_old_connections()
            self.InstanceCompra.qrcode = qrcodeReturn
            self.InstanceCompra.save()

            return True, StrErr
        except Exception as e:
            StrErr = 'erro:->[__createQrcode__] ' + StrErr + e.args[0]
            return False, StrErr
    def __createMensagem__(self) -> bool:
        try:
            StrErr: str = ''
            result: bool
            JsonMensagem:dict = json.loads(self.InstanceCompra.dados_requisicao.replace("'", "\""))
            ObjectJsonMensagem: TJSONGetProdutoFinal =  TJSONGetProdutoFinal.from_dict(JsonMensagem)
            if ObjectJsonMensagem.service_name == 'LoveGeneration Premium':
              result, StrErr = self.__createQrcode__(StrErr)
              if not result and StrErr != '':
                  return False, StrErr
    
            # instenceSendEmail: Sendemail = Sendemail(
            #     recipient_email= ObjectJsonMensagem.email,s
            #     subject= "Sua Pagina de Amor foi criada com sucesso!",
            #     message="Obrigado por confiar em nosso produto! Estamos enviando este e-mail com todos os detalhes para você. Temos certeza de que sua amada ou amado vai adorar essa surpresa especial.",
            #     FileQrcode= self.InstanceCompra.qrcode if self.InstanceCompra.qrcode else None, 
            #     link= self.InstanceCompra.linkLove
            # ) 
            # instenceSendEmail.send_email()


            linkPagina: str = self.link
            instanceEmail = EmailSender()
            instanceEmail.send_emails(
                link=linkPagina,
                fileQrcode=self.InstanceCompra.qrcode if self.InstanceCompra.qrcode else None,
                idCompra= self.InstanceCompra.token_referencia,
            )
            return True, StrErr
        
        except Exception as e:
            StrErr += '__createMensagem__ erro->' + e.args[0]
            return False, StrErr
