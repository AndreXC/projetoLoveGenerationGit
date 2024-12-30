from django.contrib import admin
from .models import Compra, Arquivo, paymentNotProcess, Error, PageNotCarregadaErro

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'token_referencia', 'status_compra', 'dados_requisicao', 'clienteId', 'TokenLove', 'qrcode', 'SendEmailCliente')  
    search_fields = ('token_referencia', 'status_compra', 'SendEmailCliente')  
    list_filter = ('status_compra','token_referencia', 'SendEmailCliente',)


@admin.register(Arquivo)
class ArquivoAdmin(admin.ModelAdmin):
    list_display = ('nome_arquivo', 'arquivo', 'id_cliente', 'dateCreate')
    search_fields = ('nome_arquivo',)


@admin.register(paymentNotProcess)
class PaymentNotProcessAdmin(admin.ModelAdmin):
    list_display = ('token_referencia', 'status_compra', 'clienteId', 'details')  # Campos para exibir na listagem
    search_fields = ('token_referencia', 'status_compra')  # Campos para pesquisa no admin





@admin.register(Error)
class Error(admin.ModelAdmin):
    list_display = ('error_type', 'details', 'occurred_at')




@admin.register(PageNotCarregadaErro)
class pageNotCarregadaError(admin.ModelAdmin):
    list_display = ('token_referencia', 'error_type', 'occurred_at')
