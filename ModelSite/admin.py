from django.contrib import admin
from .models import Compra, Arquivo, paymentNotProcess

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'token_referencia', 'status_compra', 'dados_requisicao', 'clienteId', 'TokenLove', 'qrcode')  
    search_fields = ('token_referencia', 'status_compra')  
    list_filter = ('status_compra','token_referencia',)


@admin.register(Arquivo)
class ArquivoAdmin(admin.ModelAdmin):
    list_display = ('nome_arquivo', 'arquivo', 'id_cliente', 'dateCreate')
    search_fields = ('nome_arquivo',)


@admin.register(paymentNotProcess)
class PaymentNotProcessAdmin(admin.ModelAdmin):
    list_display = ('token_referencia', 'status_compra', 'clienteId', 'details')  # Campos para exibir na listagem
    search_fields = ('token_referencia', 'status_compra')  # Campos para pesquisa no admin