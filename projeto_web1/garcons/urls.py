from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("list_pedidos/", views.list_pedidos, name="list_pedidos"),
    path("fazer_pedido/", views.fazer_pedido, name="fazer_pedido" ),
    
]