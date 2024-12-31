import os
import random

link_save_arq_final = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/img/imgUsers')
link_save_arq_temp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/img/temp').replace('\\comuns', '')


LinkSaveQrcode= r'structureproject\static\Img\SavetempQrcode'
QrcodePath = r'structureproject\static\Img\qrcode\QrcodeModelo.png'

dict_services: dict[str, str] = {
    8.0: 'LoveGeneration standard', 
    12.0: 'LoveGeneration Premium' 
}

moeda: str = "BRL"
idpadrao: str = "1"
quantidadePadrao: int = 1

HostPagina= 'https://lovegeneration.pythonanywhere.com'


def getMensagens(tamListFotos: int):
    # Lista de mensagens românticas
    mensagens: list[str] = [
        "Seu sorriso me cativa.",
        "Amo seu olhar.",
        "Nós nascemos um para o outro.",
        "Você ilumina meus dias.",
        "Meu coração é seu.",
        "Você é minha razão de sorrir.",
        "Seu jeito é único e especial.",
        "Estar ao seu lado é o meu lugar favorito.",
        "Você é meu sonho realizado.",
        "Amo cada detalhe seu."
    ]
    
    # Gerar uma lista com mensagens aleatórias
    mensagens_aleatorias:list = random.sample(mensagens, min(tamListFotos, len(mensagens)))
    return mensagens_aleatorias
    

