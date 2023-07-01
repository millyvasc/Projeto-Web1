from django.urls import path
from . import views

urlpatterns = [
    path("<int:mesa1>/adicionar/<int:cod_produto>/", views.adicionar, name="adicionar"),
    path("<int:mesa1>/carrinho/", views.list_carrinho, name="list_carrinho"),
    path("<int:mesa1>/carrinhoRemover/<int:cod_produto>/",
         views.remover_carrinho_confirmar, name="remover_carrinho_confirmar"),
    path("<int:mesa1>/confirmarPedidoFinal/<int:cod_pedido>/",
         views.confirmarPedidoFinal, name="confirmarPedidoFinal"),
    path("<int:mesa1>/modificar/<int:cod_pedido>/", views.modificarPedido, name="modificarPedido"),
    path("<int:mesa1>/cancelar/<int:cod_pedido>/", views.deletarPedido, name="deletarPedido"),
    path("<int:mesa1>/cancelarFinal/<int:cod_pedido>/", views.deletarPedidoFinal, name="deletarPedidoFinal"),

    path("<int:mesa1>/comanda/", views.fecharConta, name="fecharConta"),
]
