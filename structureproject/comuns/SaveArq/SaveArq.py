import uuid
from django.core.files.storage import FileSystemStorage
import os

class FileStorage:
    def __init__(self, caminho:str) -> None:
        self.caminho= caminho
        self.ListReturn: list = []

    def set_storage(self):
        self.storage = FileSystemStorage(location=self.caminho)

    def generate_unique_filename(self, original_name: str) -> str:
        # Gera um UUID e obtém a extensão do arquivo original
        ext = os.path.splitext(original_name)[1]
        unique_name = f"{uuid.uuid4()}{ext}"  # Gera um nome único
        return unique_name

    def save_files(self, file_list: list):
        if not self.storage:
            raise ValueError("Storage location is not set. Call set_storage() first.")
        
        for file in file_list:
            unique_name = self.generate_unique_filename(file.name)  # Gera um nome único
            self.storage.save(unique_name, file)  # Salva o arquivo com o novo nome
            self.ListReturn.append(unique_name)  # Armazena o novo nome na lista
        
        return self.ListReturn  # Retorna a lista de novos nomes de arquivos

# Exemplo de uso
def save_arq(file_list: list, caminho: str):
    file_storage = FileStorage(caminho)
    file_storage.set_storage()  # Define o caminho
    return file_storage.save_files(file_list)  # Retorna a lista de novos nomes de arquivos
