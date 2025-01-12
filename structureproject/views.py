from django.shortcuts import render, redirect
from django.http import JsonResponse
from .comuns.comuns import dict_services, moeda, idpadrao, quantidadePadrao, HostPagina, getMensagens   
from .dto.Jsonobjetoproduto import TJsonProdutosPost
from .dto.jsontoobjectGetproduto import TJSONGetProduto
from .utils.pagamento.Payment import PaymentLinkGenerator
from .utils.checandoPagamento.checkPayment import PaymentCheck
from typing import Union
from ModelSite.models import Compra, Error, paymentNotProcess, PageNotCarregadaErro, tokenApi
from django.views.decorators.csrf import csrf_exempt
import json
from .comuns.SaveArqBd.SaveArqBd import SaveArquivosBlob
from .comuns.PageFlorIcon.pageFIc import extractFlorArq, extractIconLogo  
import base64
from .dto.JsonGetProdutoStatusCompra import PaymentData
from .utils.Status_compra.statusCompra import OrdemStatusService 
from django.db import close_old_connections





def index(request):
    return render(request, 'index.html')


def ViewProdutoStatus(request):
    return render(request, 'viewproduto.html')
    

def _Status_(request):
    payment_data = {
        'collection_id': request.GET.get('collection_id'),
        'collection_status': request.GET.get('collection_status'),
        'payment_id': request.GET.get('payment_id'),
        'status': request.GET.get('status'),
        'external_reference': request.GET.get('external_reference'),
        'payment_type': request.GET.get('payment_type'),
        'merchant_order_id': request.GET.get('merchant_order_id'),
        'preference_id': request.GET.get('preference_id'),
        'site_id': request.GET.get('site_id'),
        'processing_mode': request.GET.get('processing_mode'),
        'merchant_account_id': request.GET.get('merchant_account_id'),
    }
    
    if payment_data['payment_id']:
        CheckStatusInstance: PaymentCheck = PaymentCheck(payment_data['payment_id'])
        response: dict[str, Union[str, int, bool]] = CheckStatusInstance._check_Status_payment_()
        if not response:
            close_old_connections()
            instancepaymentNotProcess: paymentNotProcess = paymentNotProcess(
                token_referencia=payment_data['external_reference'],
                status_compra=payment_data['status'],
                clienteId= payment_data['payment_id'],
                details='Response Vazio'
            )
            instancepaymentNotProcess.save()
            return render(request, 'index.html', {'CompraErro':True, 'id': payment_data['payment_id'], 'ExternalReference': payment_data['external_reference']})
        
        instanciaOrdemStatusService:OrdemStatusService =  OrdemStatusService()
        result, StrErr, status = instanciaOrdemStatusService.process_response(payment_data['payment_id'], response)
        if not result and StrErr != '':
            InstanceCompraCliente= PaymentData.from_json(response)
            close_old_connections()
            instancepaymentNotProcess: paymentNotProcess = paymentNotProcess(
                token_referencia=InstanceCompraCliente.external_reference,
                status_compra=InstanceCompraCliente.status,
                clienteId=payment_data['payment_id'],
                details='Erro: ' + str(StrErr)
            )
            instancepaymentNotProcess.save()
            return render(request, 'index.html', {'CompraErro':True, 'id': payment_data['payment_id'], 'ExternalReference': payment_data['external_reference']})
        if status != '':
           return render(request, 'index.html', {'Compra':True, 'StatusCompra': status})
        return render(request, 'index.html', {'Compra_':True, 'ExternalReference': payment_data['external_reference']})

    



def CreatePayment(request):
    try:
        PostServicesPayment = TJsonProdutosPost(
            idpadrao,
            request.session['Mensagem']['serviceName'],
            quantidadePadrao,
            moeda,
            request.session['Mensagem']['service'] 
        ).to_dict()

        PaymentInstance: PaymentLinkGenerator= PaymentLinkGenerator()
        response: dict[str, Union[str, int, bool]] = PaymentInstance.gerar_link_pagamento(PostServicesPayment)
        if not response:
            request.session['Mensagem'].clear()    
            return render(request, 'index.html', {'CreatePaymentError': True})
        
        objectResultProduto= TJSONGetProduto.from_dict(response)
        close_old_connections()
        instanciaCompra:Compra = Compra(
        token_referencia=objectResultProduto.external_reference,  
            status_compra="Pendente",    
            dados_requisicao=f"{request.session['Mensagem']}"
        )
        instanciaCompra.save()

    
        return redirect(objectResultProduto.init_point)
    
    except Exception as e:
        close_old_connections()
        instanceError: Error = Error(
                error_type=type(e).__name__,
                details=e.args[0]
            )
        instanceError.save()
        request.session['Mensagem'].clear()
        return render(request, 'index.html', {'CreatePaymentError': True})




def love_message_view(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        mensagem = request.POST.get('mensagem')
        servicevalor = float(request.POST.get('service'))
        flor = request.POST.get('flower')
        images = request.FILES.getlist('images[]')
        data =  request.POST.get('date')
        hour = request.POST.get('hour')
        
        
        #salvar os arquivos no Banco.
        instanceSaveArquivosBlob:SaveArquivosBlob = SaveArquivosBlob()
        result, StrErr, idClient = instanceSaveArquivosBlob.__insertArq__(images)

        if not result and StrErr != '':
            close_old_connections()
            instanceError: Error = Error(
                error_type= '__insertArq__',
                details=StrErr
            )
            instanceError.save()
            return JsonResponse({'status': 'error', 'message': 'Estamos Com um erro interno, por favor, tente novamente Depois!'})
            
                
        # imagesList:list[str]= save_arq(images, link_save_arq_temp)
        servicename = dict_services[servicevalor] 
      
        #Gera um dicionário com os dados recebidos
        request.session['Mensagem'] = {
            'nome': nome,   
            'email': email,
            'mensagem': mensagem,
            'service': servicevalor,
            'flor': flor,
            'data': data,
            'hour': hour,
            'idfotosSalvas': idClient, 
            'serviceName': servicename, 
        } 

        return JsonResponse({'status': 'success', 'redirect_url': 'CreatePayment'})
    
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'})




@csrf_exempt
def mercado_pago_webhook(request):
    if request.method == "POST":
        data = json.loads(request.body)
        payment_id = data.get("data", {}).get("id")
        topic =  data.get("type")

        # Verifica se a notificação é sobre um pagamento
        if topic == "payment" and payment_id:
            CheckStatusInstance: PaymentCheck = PaymentCheck(payment_id)
            response: dict[str, Union[str, int, bool]] = CheckStatusInstance._check_Status_payment_()

            if not response:
               return JsonResponse({"status": "error", "message": "response vazio"}, status=400)
            
            instanciaOrdemStatusService:OrdemStatusService =  OrdemStatusService()
            result, StrErr, status = instanciaOrdemStatusService.process_response(payment_id, response)
            if not result and StrErr != '':
                InstanceCompraCliente= PaymentData.from_json(response)
                close_old_connections()
                instancepaymentNotProcess: paymentNotProcess = paymentNotProcess(
                    token_referencia=InstanceCompraCliente.external_reference,
                    status_compra=InstanceCompraCliente.status,
                    clienteId=payment_id,
                    details='Erro: ' + str(StrErr)
                )
                instancepaymentNotProcess.save()
                return JsonResponse({"status": "failed"}, status=400)
    
            # Confirma que o webhook foi processado
            return JsonResponse({"status": "success"}, status=200)
           
    # Retorna erro se a notificação não for válida
    return JsonResponse({"status": "failed"}, status=400)


def CreatePage(request, referencia, token):
    try:
        close_old_connections()
        InstanceCliente: Compra = Compra.objects.get(token_referencia=referencia, TokenLove= token)
        if InstanceCliente.status_compra == 'approved':
            JsonMensagem: json = json.loads(InstanceCliente.dados_requisicao.replace("'", "\""))            
            
            instanciaExtractFlor: extractFlorArq =  extractFlorArq()
            result, strErr, flor = instanciaExtractFlor.__extractArqAll__(id= JsonMensagem['flor']) 
            
            if not result and strErr !='':
                close_old_connections()
                instancePageNotCarregadaErro: PageNotCarregadaErro = PageNotCarregadaErro
                instancePageNotCarregadaErro.objects.create(
                    token_referencia = referencia, 
                    error_type = strErr
                )
                instancePageNotCarregadaErro.save()
                return render(request, 'index.html', {'PageNotCarregadaErro': True, 'referenciaToken': referencia})
            


            instanceIconLogoPage: extractIconLogo = extractIconLogo()
            result, strErr,logo, icon = instanceIconLogoPage.__extractArqAll__(id=1)


            if not result and strErr !='':
                close_old_connections()
                instancePageNotCarregadaErro: PageNotCarregadaErro = PageNotCarregadaErro
                instancePageNotCarregadaErro.objects.create(
                    token_referencia = referencia, 
                    error_type = strErr
                )
                instancePageNotCarregadaErro.save()
                return render(request, 'index.html', {'PageNotCarregadaErro': True, 'referenciaToken': referencia})
            


            instanceSaveTblob: SaveArquivosBlob = SaveArquivosBlob()
            result, strErr, images = instanceSaveTblob.__extractArqAll__(JsonMensagem['idfotosSalvas'])
            if not result and strErr !='':
                close_old_connections()
                instancePageNotCarregadaErro: PageNotCarregadaErro = PageNotCarregadaErro
                instancePageNotCarregadaErro.objects.create(
                    token_referencia = referencia, 
                    error_type = strErr
                )
                instancePageNotCarregadaErro.save()
                return render(request, 'index.html', {'PageNotCarregadaErro': True, 'referenciaToken': referencia})
            

            ListaMensagens:list[str] = getMensagens(len(images))
            imageAndMensagens: list[str] = zip(images, ListaMensagens)

            return render(request, 'LovePage.html', {'JsonMensagem':JsonMensagem, 'dadosImageMensagem':imageAndMensagens, 'flor': flor, 'icon': icon, 'logo': logo})
               
    except Compra.DoesNotExist:
        return render(request, 'PageNotFound.html')
    
    
    
def search_produto(request):
    order_id = request.GET.get('id')
    try:
        close_old_connections()
        order = Compra.objects.get(token_referencia= order_id)
        
        qrcode_data = None
        if order.qrcode:
            qrcode_data = base64.b64encode(order.qrcode).decode('utf-8')

        link:str = HostPagina + f'/Pagina/{order.token_referencia}/{order.TokenLove}'
        data = {
            'order': {
                'link':link, 
                'status': order.status_compra,
                'clienteId': order.clienteId,
                'gerado': order.created_at,
                'qrcode': qrcode_data
            }
        }
        return JsonResponse(data)
    except Compra.DoesNotExist:
        return JsonResponse({'order': None}, status=404)




# View para lidar com a página 404 personalizada
def custom_page_not_found(request, exception):
    return render(request, 'PageNotFound.html', status=404)




def GetCompras(request, token):
    try:
        if not tokenApi.objects.filter(token=token).exists():
            return JsonResponse({'tokenInvalido': True}, status=404)

        compras: Compra = Compra.objects.all()
        
        compras_lista:list[dict] = [
            {
                "token_referencia": compra.token_referencia,
                "status_compra": compra.status_compra,
                "dados_requisicao": compra.dados_requisicao,
                "created_at": compra.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "updated_at": compra.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                "clienteId": compra.clienteId,
                "TokenLove": compra.TokenLove,
                "qrcode": base64.b64encode(compra.qrcode).decode('utf-8') if compra.qrcode else None,
                "SendEmailCliente": compra.SendEmailCliente,
            }
            for compra in compras
        ]

        return JsonResponse(compras_lista, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


