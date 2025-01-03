from ModelSite.models import florArq, iconLogoPage
import base64
from django.db import close_old_connections


class extractFlorArq:
    def __init__(self):
        self.StrErr: str =  ''
        self.instanciaflorArq: florArq = florArq

        
    def __extractArqAll__(self, id: str):
        try:
            idflower:int = 0 
            match id:
                case 'flower1':
                    idflower=3
                case 'flower2':
                    idflower= 2
                case 'flower3':
                    idflower= 1
            
        
            close_old_connections()
            florE = self.instanciaflorArq.objects.filter(idflor=idflower)


            for arquivo in florE:
                # Converte o conteúdo binário em uma URL de dados
                if arquivo.flor:
                    flor64 = base64.b64encode(arquivo.flor).decode('utf-8')
                    flor = f"data:image/jpeg;base64,{flor64}" 
                

            return True, '', flor

        except Exception as e:
            self.StrErr = f'[SaveArquivosBlob]-> __extractArqAll__ erro: {e.__context__} : {e.args[0]}'
            return False, self.StrErr, []
           
           


class extractIconLogo:
    def __init__(self):
        self.StrErr: str =  ''
        self.instanciaPgeIconLogo: iconLogoPage = iconLogoPage

        
    def __extractArqAll__(self, id: int):
        try:
            close_old_connections()
            Page = self.instanciaPgeIconLogo.objects.filter(idLogoicon=id)
            imagens = []

            for arquivo in Page:
                icon64link = f"data:image/jpeg;base64,{base64.b64encode(arquivo.icon).decode('utf-8')}"
                logo64link = f"data:image/jpeg;base64,{base64.b64encode(arquivo.logo).decode('utf-8')}"

            return True, '', icon64link, logo64link

        except Exception as e:
            self.StrErr = f'[SaveArquivosBlob]-> __extractArqAll__ erro: {e.__context__} : {e.args[0]}'
            return False, self.StrErr, []
