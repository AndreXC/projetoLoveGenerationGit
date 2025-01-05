import qrcode
from PIL import Image
from ModelSite.models import Error, QrcodeBinary
from io import BytesIO
import tempfile
import os
from django.db import close_old_connections

def QrcodeModel():
    """
    Extrai a imagem binária do banco e a salva como um arquivo PNG temporário.
    Retorna o caminho para o arquivo temporário.
    """
    try:
        close_old_connections()
        # Recupera os dados binários da imagem no banco
        qrcodeModel = QrcodeBinary.objects.get(idqrcode=1)
        qrcode_binary = qrcodeModel.qrcode

        # Cria um arquivo temporário para salvar a imagem como PNG
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
            # Abre os dados binários como uma imagem
            img = Image.open(BytesIO(qrcode_binary))
            # Salva a imagem no arquivo temporário
            img.save(temp_file.name, format='PNG')
            return temp_file.name  # Retorna o caminho do arquivo
    except Exception as e:
        close_old_connections()
        Error.objects.create(
            error_type=type(e).__name__,
            details=f'[QrcodeModel()] {str(e)}'
        )
        raise


class QRCodeGenerator:
    def __init__(self):
        self.scale_factor = 0.6
        self.angle = 45

    def generate_qr_code(self, data: str) -> tuple[bool, str]:
        try:
            # Gerar o QR Code diretamente como imagem
            qr_img = qrcode.make(data).convert('RGBA')

            # Aumentar o tamanho do QR Code
            qr_img = qr_img.resize(
                (int(qr_img.width * self.scale_factor), int(qr_img.height * self.scale_factor)),
                Image.LANCZOS  # Melhor qualidade de redimensionamento
            )

            # Inclinar o QR Code
            qr_img = qr_img.rotate(self.angle, expand=True)

            # Criar uma nova imagem com fundo transparente
            qr_img_with_transparency = Image.new("RGBA", qr_img.size, (255, 255, 255, 0))
            qr_img_with_transparency.paste(qr_img, (0, 0), qr_img)

            # Obter o caminho da imagem da moldura extraída do banco
            QrcodePath = QrcodeModel()

            # Abrir a imagem da moldura e colar o QR Code
            with Image.open(QrcodePath) as frame_img:
                # Calcular a posição para centralizar o QR Code
                position = (
                    (frame_img.width - qr_img_with_transparency.width) // 2 + 3,
                    (frame_img.height - qr_img_with_transparency.height) // 2 + 95
                )
                frame_img.paste(qr_img_with_transparency, position, qr_img_with_transparency)

                buffer = BytesIO()
                # Salvar a imagem com o QR Code no local de saída com extensão .png
                frame_img.save(buffer, format='PNG')  # Você pode usar outro formato, como JPG
                buffer.seek(0)

                # Limpar o arquivo temporário
                os.remove(QrcodePath)

                return True, '', buffer.read()

        except Exception as e:
            close_old_connections()
            Error.objects.create(
                error_type=type(e).__name__,
                details=f'[QRCodeGenerator] {str(e)}'
            )
            return False, f'[QRCodeGenerator]-> erro {str(e)}'
