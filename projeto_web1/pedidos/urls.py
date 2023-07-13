from django.urls import path
from . import views

urlpatterns = [
#     path("<int:mesa1>/adicionar/<int:cod_produto>/", views.adicionar, name="adicionar"),
    path("carrinho/", views.list_carrinho, name="list_carrinho"),
    path("carrinhoRemover/<int:cod_produto>/",
         views.remover_carrinho_confirmar, name="remover_carrinho_confirmar"),
    path("confirmarPedidoFinal/<int:cod_pedido>/",
         views.confirmarPedidoFinal, name="confirmarPedidoFinal"),
    path("modificar/<int:cod_pedido>/", views.modificarPedido, name="modificarPedido"),
    path("cancelar/<int:cod_pedido>/", views.deletarPedido, name="deletarPedido"),
    path("cancelarFinal/<int:cod_pedido>/", views.deletarPedidoFinal, name="deletarPedidoFinal"),
    path("adicionar/<int:cod_produto>/", views.adicionar, name="adicionar"),
    

]
