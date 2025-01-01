import qrcode
from PIL import Image
import secrets
from ModelSite.models import Error
from io import BytesIO

QrcodePath = r'static\Img\qrcode\QrcodeModelo.png'
 
class QRCodeGenerator:
    def __init__(self):
        self.scale_factor = 0.6
        self.angle = 45
        self.OutputQrcode:str = secrets.token_hex(20)

    
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

                return True , '', buffer.read()

        except Exception as e:
            Error.objects.create(
            error_type=type(e).__name__,
            details='[QRCodeGenerator]'+ e.args[0])
            return False, f'[QRCodeGenerator]-> erro {e.args[1]}'

