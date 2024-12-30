from django.contrib import admin
from django.urls import path
from .views import index, love_message_view, CreatePayment, mercado_pago_webhook, CreatePage, ViewProdutoStatus, search_produto, _Status_ , custom_page_not_found
from django.conf import settings
from django.conf.urls.static import static  
from django.urls import re_path
from django.views.static import serve
from . import views
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='Index'),  
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('CreateMenssage', love_message_view, name='Checkin'),
    path('CreatePayment', CreatePayment, name='CreatePayment'),
    path('Pagina/<str:referencia>/<str:token>/', CreatePage, name='CreatePage'),
    path ('falilure', _Status_, name='Paymentfalilure' ),
    path ('Pending', _Status_, name='PaymentPending' ),
    path ('Aproved', _Status_, name='PaymentAproved' ),
    path('api/webhook/', mercado_pago_webhook, name='mercado_pago_webhook'),
    path('produto/visualizar/', ViewProdutoStatus, name='produtoVisualizar'),
    path('api/search_produto/', search_produto, name='search_produto'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = custom_page_not_found
# Configuração para usar a view personalizada para erro 404

