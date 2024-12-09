import json
from ModelSite.models import Compra, Error, paymentNotProcess
from utils.posPayment.posPagamento import createEstruturaProject
from utils.Paymentpending.paymentpending import PaymentPending
from dto.JsonGetProdutoStatusCompra import PaymentData
from comuns.SaveArqBd.SaveArqBd import SaveArquivosBlob

class OrderStatusHandler:
    def __init__(self, payment_service, storage_service):
        self.payment_service:createEstruturaProject = payment_service
        self.storage_service: SaveArquivosBlob= storage_service

    def approved(self, compra_cliente: Compra) -> None:
        try:
            result, str_err = self.payment_service.__createMensagem__(compra_cliente.token_referencia)
            if not result:
                raise ValueError(str_err)
        except Exception as e:
            payment_not_processed = paymentNotProcess(
                token_referencia=compra_cliente.token_referencia,
                status_compra=compra_cliente.status_compra,
                clienteId=compra_cliente.clienteId,
                details=f"Erro: {e}",
            )
            payment_not_processed.save()

    def pending(self, compra_cliente: Compra, produto_data: PaymentData) -> None:
        try:
            json_message = json.loads(compra_cliente.dados_requisicao.replace("'", "\""))
            email_status = self.payment_service.send_email(
                email=json_message['email'], 
                qrcode=produto_data.qr_code,
                name=produto_data.name,
                external_reference=compra_cliente.token_referencia,
            )
            if not email_status:
                raise ValueError("Falha ao enviar email.")
        except Exception as e:
            error = Error(error_type="PaymentPending", details=str(e))
            error.save()

    def rejected(self, compra_cliente: Compra) -> None:
        try:
            json_message = json.loads(compra_cliente.dados_requisicao.replace("'", "\""))
            self.storage_service.extract_all_files(json_message['idfotosSalvas'])
        except Exception as e:
            error = Error(error_type="FileExtraction", details=str(e))
            error.save()
