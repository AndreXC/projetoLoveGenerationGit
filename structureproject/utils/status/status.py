from typing import Tuple, Any
from ModelSite.models import Compra
from ...utils.posPayment.posPagamento import createEstruturaProject
import json
from ...utils.Paymentpending.paymentpending import PaymentPending
from ...utils.PaymentRejected.paymentRejected  import PaymentRejected
from ...dto.JsonGetProdutoStatusCompra import PaymentData
from ...comuns.SaveArqBd.SaveArqBd import SaveArquivosBlob
from django.db import close_old_connections


class CompraRepository:
    """Responsável por interações com a base de dados relacionadas às compras."""
    def get_compra(self, external_reference: str) -> Compra:
        try:
            close_old_connections()            
            return Compra.objects.get(token_referencia=external_reference)
        except Compra.DoesNotExist:
            raise ValueError("Compra não encontrada para o token fornecido.")


class PaymentProcessor:
    """Processador de pagamentos com a lógica específica para cada situação."""
    def __init__(self):
        self.compra_repository = CompraRepository()

    def handle_approved(self, external_reference: str, payment_id: str) -> Tuple[bool, Any]:
        try:
            compra = self.compra_repository.get_compra(external_reference)
            compra.status_compra = "approved"
            compra.clienteId = payment_id
            compra.save()

            pos_payment_instance = createEstruturaProject(external_reference)
            result, StrErr = pos_payment_instance.__createMensagem__()
            
            return result, StrErr
        except Exception as e:
            return False, f"Erro ao processar pagamento aprovado: {e}"

    def handle_pending(self, external_reference: str, payment_data: PaymentData) -> Tuple[bool, Any]:
        try:
            compra = self.compra_repository.get_compra(external_reference)
            compra.status_compra = "pending"
            compra.save()

            json_message = json.loads(compra.dados_requisicao.replace("'", "\""))
            payment_pending_instance = PaymentPending(
                Email=json_message['email'],
                qrcode=payment_data.qr_code,
                name=payment_data.name,
                tokenReference=compra.token_referencia,
            )
            result, StrErr = payment_pending_instance.__SendEmailPending__()
            return result, StrErr
        except Exception as e:
            return False, f"Erro ao processar pagamento pendente: {e}"

    def handle_rejected(self, external_reference: str) -> Tuple[bool, Any]:
        try:
            compra = self.compra_repository.get_compra(external_reference)
            compra.status_compra = "rejected"
            compra.save()

            json_message = json.loads(compra.dados_requisicao.replace("'", "\""))
            save_blob_instance = SaveArquivosBlob()
            result, StrErr = save_blob_instance.__delete__(json_message['idfotosSalvas'])
            payment_Rejected_instance = PaymentRejected(
                Email=json_message['email'],
                tokenReference=compra.token_referencia,
            )
            result, StrErr = payment_Rejected_instance.__SendEmailRejected__()        
            
            return result, StrErr 
        except Exception as e:
            return False, f"Erro ao processar pagamento rejeitado: {e}"


class OrdemStatusService:
    """Classe principal de controle, orquestrando a lógica de pagamentos com abstração."""
    def __init__(self):
        self.Instancepayment_processor:PaymentProcessor = PaymentProcessor()
      

    def process_response(self, payment_id: str, response: dict) -> Tuple[bool, Any]:
        try:
            object_result = PaymentData.from_json(response)
            status = object_result.status
            match status: 
                case "approved":
                    result, strErr = self.Instancepayment_processor.handle_approved(object_result.external_reference, payment_id)
                    return  result, strErr, status
                case "pending":
                    result, strErr = self.Instancepayment_processor.handle_pending(object_result.external_reference, object_result)
                    return  result, strErr, status
                case "rejected":
                    result, strErr= self.Instancepayment_processor.handle_rejected(object_result.external_reference, object_result)
                    return  result, strErr, status
        except Exception as e:
            return False,  f"Erro ao processar resposta: {e.args[1]}", status 
