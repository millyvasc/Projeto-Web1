from django.urls import path
from . import views

urlpatterns = [

    path("carrinho/", views.list_carrinho, name="list_carrinho"),
    path("carrinhoRemover/<int:cod_produto>/",
         views.remover_carrinho_confirmar, name="remover_carrinho_confirmar"),
    path("confirmarPedidoFinal/<int:cod_pedido>/",
         views.confirmarPedidoFinal, name="confirmarPedidoFinal"),
    path("modificar/<int:cod_pedido>/", views.modificarPedido, name="modificarPedido"),
    path("cancelar/<int:cod_pedido>/", views.deletarPedido, name="deletarPedido"),
    path("cancelarFinal/<int:cod_pedido>/", views.deletarPedidoFinal, name="deletarPedidoFinal"),
    path("adicionar/<int:cod_produto>/", views.adicionar, name="adicionar"),
    
    # ------------------------------ Referentes a garçom ----------------------------------------------
    path("list_pedidos/", views.list_pedidos, name="list_pedidos"),
    path('<int:cod_comanda>/<int:cod_pedido>/describe_pedido/', views.describe_pedido, name='describe_pedido'),
    path("<int:codigo_pedido>/entregar_pedido/", views.changeStatusPedido, name="entregar_pedido"),

]
