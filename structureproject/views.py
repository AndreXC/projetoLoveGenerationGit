from django.shortcuts import render, redirect
from django.http import JsonResponse
from .comuns.comuns import dict_services, moeda, idpadrao, quantidadePadrao, HostPagina, getMensagens   
from .dto.Jsonobjetoproduto import TJsonProdutosPost
from .dto.jsontoobjectGetproduto import TJSONGetProduto
from .dto.JsonGetProdutoStatusCompra import PaymentData
from .utils.pagamento.Payment import PaymentLinkGenerator
from .utils.checandoPagamento.checkPayment import PaymentCheck
from typing import Union
from ModelSite.models import Compra, Error, paymentNotProcess, PageNotCarregadaErro

from django.views.decorators.csrf import csrf_exempt
import json
from .utils.posPayment.posPagamento import createEstruturaProject
from .utils.Paymentpending.paymentpending import PaymentPending
from .comuns.SaveArqBd.SaveArqBd import SaveArquivosBlob
import base64




def index(request):
    return render(request, 'teste.html')


def ViewProdutoStatus(request):
    return render(request, 'viewproduto.html')
    
        


# def _PaymentAproved_(request):
#     payment_data = {
#         'collection_id': request.GET.get('collection_id'),
#         'collection_status': request.GET.get('collection_status'),
#         'payment_id': request.GET.get('payment_id'),
#         'status': request.GET.get('status'),
#         'external_reference': request.GET.get('external_reference'),
#         'payment_type': request.GET.get('payment_type'),
#         'merchant_order_id': request.GET.get('merchant_order_id'),
#         'preference_id': request.GET.get('preference_id'),
#         'site_id': request.GET.get('site_id'),
#         'processing_mode': request.GET.get('processing_mode'),
#         'merchant_account_id': request.GET.get('merchant_account_id'),
#     }
#     PaymentAprovedCard.objects.create(**payment_data)




def CreatePayment(request):
    try:
        PostServicesPayment = TJsonProdutosPost(
            idpadrao,
            request.session['Mensagem']['serviceName'],
            quantidadePadrao,
            moeda,
            1.0
        ).to_dict()

        PaymentInstance: PaymentLinkGenerator= PaymentLinkGenerator()
        response: dict[str, Union[str, int, bool]] = PaymentInstance.gerar_link_pagamento(PostServicesPayment)

        if not response:
            request.session['Mensagem'].clear()    
            return render(request, 'index.html', {'CreatePaymentError': True})
        
        objectResultProduto= TJSONGetProduto.from_dict(response)
        Compra.objects.create(
        token_referencia= objectResultProduto.external_reference,  
        status_compra="Pendente",    
        dados_requisicao= f"{request.session['Mensagem']}"
        )
    
        return redirect(objectResultProduto.init_point)
    
    except Exception as e:
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
           
            objectResultProduto:PaymentData = PaymentData.from_json(response)
            InstanceCompraCliente: Compra = Compra.objects.get(token_referencia=objectResultProduto.external_reference)
            match objectResultProduto.status:
                case 'approved':
                    InstanceCompraCliente.status_compra = "approved"
                    InstanceCompraCliente.clienteId =  payment_id
                    InstanceCompraCliente.save()
                    instancePosPayment : createEstruturaProject =  createEstruturaProject(InstanceCompraCliente.token_referencia)
                    result, StrErr = instancePosPayment.__createMensagem__()
                    if not result and StrErr != '':
                        instancepaymentNotProcess: paymentNotProcess = paymentNotProcess(
                            token_referencia=InstanceCompraCliente.token_referencia,
                            status_compra=InstanceCompraCliente.status_compra,
                            clienteId=InstanceCompraCliente.clienteId,
                            details='Erro: ' + str(StrErr)
                        )
                        instancepaymentNotProcess.save()
                        return JsonResponse({"status": "failed"}, status=400)
                case 'pending':
                    InstanceCompraCliente.status_compra = "pending" 
                    InstanceCompraCliente.save()

                    JsonMensagem:dict = json.loads(InstanceCompraCliente.dados_requisicao.replace("'", "\""))
                    instancePaymentPending:PaymentPending = PaymentPending(email=JsonMensagem['email'], qrcode=objectResultProduto.qr_code, name=objectResultProduto.name, external_reference=InstanceCompraCliente.token_referencia)
                    result, StrErr = instancePaymentPending.__SendEmail__()
                    if not result and StrErr !='':
                        instanceError: Error = Error(
                                error_type= 'PaymentPendingClass',
                                details=StrErr
                            )
                        instanceError.save()

                case 'rejected':
                    InstanceCompraCliente.status_compra = 'rejected' 
                    InstanceCompraCliente.save()

                    JsonMensagem: json = json.loads(InstanceCompraCliente.dados_requisicao.replace("'", "\""))
                    instanceSaveTblob: SaveArquivosBlob = SaveArquivosBlob()
                    result, StrErr = instanceSaveTblob.__extractArqAll__(JsonMensagem['idfotosSalvas'])
                    if not result and StrErr !='':
                        instanceError: Error = Error(
                                error_type= 'instanceSaveTblob.__extractArqAll__',
                                details=StrErr
                            )
                        instanceError.save()
    


            # Confirma que o webhook foi processado
            return JsonResponse({"status": "success"}, status=200)

    # Retorna erro se a notificação não for válida
    return JsonResponse({"status": "failed"}, status=400)


def CreatePage(request, referencia, token):
    try:
        #Buscar  o registro no banco de dados pelo token
        InstanceCliente: Compra = Compra.objects.get(token_referencia=referencia, TokenLove= token)
        if InstanceCliente.status_compra == 'approved':
            #transformando json String em json valido
            JsonMensagem: json = json.loads(InstanceCliente.dados_requisicao.replace("'", "\""))
            
            instanceSaveTblob: SaveArquivosBlob = SaveArquivosBlob()
            result, strErr, images = instanceSaveTblob.__extractArqAll__(JsonMensagem['idfotosSalvas'])
            if not result and strErr !='':
                instancePageNotCarregadaErro: PageNotCarregadaErro = PageNotCarregadaErro
                instancePageNotCarregadaErro.objects.create(
                    token_referencia = referencia, 
                    error_type = strErr
                )
                instancePageNotCarregadaErro.save()
                return render(request, 'index.html', {'PageNotCarregadaErro': True})
            

            ListaMensagens:list[str] = getMensagens(len(images))
            imageAndMensagens: list[str] = zip(images, ListaMensagens)

            return render(request, 'LovePage.html', {'JsonMensagem':JsonMensagem, 'dadosImageMensagem':imageAndMensagens})
               
    except Compra.DoesNotExist:
        return render(request, 'PageNotFound.html')
    
    
    
def search_produto(request):
    order_id = request.GET.get('id')
    try:
        order = Compra.objects.get(token_referencia= order_id)
        
        qrcode_data = None
        if order.qrcode:
            qrcode_data = base64.b64encode(order.qrcode).decode('utf-8')
    
        data = {
            'order': {
                'status': order.status_compra,
                'clienteId': order.clienteId,
                'gerado': order.created_at,
                'qrcode': qrcode_data
            }
        }
        return JsonResponse(data)
    except Compra.DoesNotExist:
        return JsonResponse({'order': None}, status=404)



