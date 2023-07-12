from django.urls import path
from . import views

urlpatterns = [
    # path("", views.list_mesas, name="list_mesas"),
    path("list_mesas/", views.list_mesas, name="list_mesas"),
    path("fazer_pedido/", views.fazer_pedido, name="fazer_pedido" ),
    path("<int:mesa1>/list_pedidos/", views.list_pedidos, name="list_pedidos" ),
    path("<int:codigo_pedido>/entregar_pedido/", views.changeStatusPedido, name="entregar_pedido"),
    
    path("<int:mesa1>/list_pedido/", views.list_pedido, name="list_pedido" ),
    
    
]