from ModelSite.models import Compra
from django.db import close_old_connections
import secrets


class ReferenceChecker:
    def __init__(self):
        self.model:Compra = Compra  

    def generate_unique_reference(self):
        """
        Gera uma referência única que não existe no banco.
        """
        close_old_connections()  # Fecha conexões antigas para evitar problemas
        reference:str = secrets.token_hex(10)  # Gera uma nova referência
        # Verifica se a referência já existe no banco
        if self.model.objects.filter(token_referencia=reference).exists():
            return self.generate_unique_reference()  
        return reference  


def create_reference():
    """
    Função que retorna uma referência única.
    """
    checker = ReferenceChecker()
    return checker.generate_unique_reference()
