from ModelSite.models import Arquivo
import secrets
import base64
from django.db import close_old_connections


class SaveArquivosBlob:
    def __init__(self):
        self.StrErr: str =  ''
        self.instanciaArquivo: Arquivo = Arquivo
        self.id: str = secrets.token_hex(10)

    def __insertArq__(self, Images: list[str]):
        try:
            close_old_connections()
            for image in Images:
                if hasattr(image, 'read'):
                    binary_content = image.read()  # Se for um arquivo aberto
                    nome_arquivo = image.name
                else:
                    with open(image, 'rb') as f:  # Se for um caminho de arquivo
                        binary_content = f.read()
                        nome_arquivo = image

                # Criando a instância do modelo Arquivo
                self.instanciaArquivo.objects.create(
                        nome_arquivo=nome_arquivo,
                        arquivo=binary_content,
                        id_cliente=self.id,  # ID de cliente gerado
                    ).save()
                                
            
            return True, self.StrErr, self.id
                    
        except Exception as e:
            self.StrErr = '[SaveArquivosBlob]-> __insertArq__: ' + 'erro: ' + e
            return False, str, ''
        
    def __extractArqAll__(self, id: str):
        try:
            arquivos = self.instanciaArquivo.objects.filter(id_cliente=id)
            imagens = []

            for arquivo in arquivos:
                # Converte o conteúdo binário em uma URL de dados
                if arquivo.arquivo:
                    imagem_base64 = base64.b64encode(arquivo.arquivo).decode('utf-8')
                    imagens.append(f"data:image/jpeg;base64,{imagem_base64}") 

            return True, '', imagens

        except Exception as e:
            self.StrErr = f'[SaveArquivosBlob]-> __extractArqAll__ erro: {e.__context__} : {e.args[0]}'
            return False, self.StrErr, []
           

    def __delete__(self, id: str):
        try:
            arquivos = self.instanciaArquivo.objects.filter(id_cliente=id)
            # Deletar os arquivos encontrados
            arquivos.delete()
            return True, ''
        
        except Exception as e:
            self.StrErr = f'[SaveArquivosBlob]-> __delete__ erro: {e.__context__} : {e.args[0]}'
            return False, self.StrErr
           
