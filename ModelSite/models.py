from django.db import models
from datetime import datetime

class PaymentAprovedCard(models.Model):
    collection_id = models.CharField(max_length=50)
    collection_status = models.CharField(max_length=50)
    payment_id = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    external_reference = models.CharField(max_length=50, null=True, blank=True)
    payment_type = models.CharField(max_length=50)
    merchant_order_id = models.CharField(max_length=50)
    preference_id = models.CharField(max_length=100)
    site_id = models.CharField(max_length=50)
    processing_mode = models.CharField(max_length=50)
    merchant_account_id = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.payment_id} - {self.status}"



    
class Compra(models.Model):
    token_referencia = models.CharField(max_length=255, unique=True, null=False, blank=False)
    status_compra = models.CharField(max_length=100, default="Pendente", null=False, blank=False)
    dados_requisicao = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    clienteId = models.CharField(max_length=50, null=True, default='')
    TokenLove = models.CharField(max_length=150, default='')
    qrcode =  models.BinaryField(null=True, blank=True, default= None)
    SendEmailCliente =  models.BooleanField(default = False)


    def __str__(self):
        return f"{self.token_referencia} - {self.status_compra}"

class Arquivo(models.Model):
    nome_arquivo = models.CharField(max_length=255)
    arquivo = models.BinaryField()
    id_cliente = models.CharField(max_length=20, default='')
    dateCreate = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.nome_arquivo
    


class Error(models.Model):
    error_type = models.CharField(max_length=100)
    details = models.TextField() 
    occurred_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.error_type}: {self.details[:50]}"



class paymentNotProcess(models.Model):
    token_referencia = models.CharField(max_length=255, unique=True, null=False, blank=False)
    status_compra = models.CharField(max_length=100, default="Pendente", null=False, blank=False)
    clienteId = models.CharField(max_length=50, null=True, default='')
    details = models.TextField()
    occurred_at = models.DateTimeField(auto_now_add=True)


class PageNotCarregadaErro(models.Model):
    token_referencia = models.CharField(max_length=255, unique=True, null=False, blank=False)
    error_type = models.CharField(max_length=100)
    occurred_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.error_type}: {self.details[:50]}"



class Qrcode(models.Model):
    token_referencia = models.CharField(max_length=255, unique=True, null=False, blank=False)
    qrcode =  models.BinaryField(null=False, blank=True)
 
 
 
 
class florArq(models.Model):
    flor = models.BinaryField()
    idflor = models.IntegerField(primary_key=True ,default=1)
    
    
class iconLogoPage(models.Model):
    icon = models.BinaryField()
    logo = models.BinaryField()
    idLogoicon = models.IntegerField(primary_key=True, default=0)

    
    
      