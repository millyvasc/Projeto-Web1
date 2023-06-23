from django.urls import path
from . import views

urlpatterns = [
    path("<int:mesa1>/adicionar/<int:cod_produto>/", views.adicionar, name="adicionar"),
    path("<int:mesa1>/carrinho/", views.list_carrinho, name="list_carrinho"),
    path("<int:mesa1>/carrinhoRemover/<int:cod_produto>/", views.remover_carrinho, name="remover_carrinho"),
    path("<int:mesa1>/carrinhoRemoverConfirmar/<int:cod_produto>/", views.remover_carrinho_confirmar, name="remover_carrinho_confirmar"),
    path("<int:mesa1>/fazerPedido/<int:cod_pedido>/", views.fazer_pedido, name="fazer_pedido"),
    #path("<int:produto_cod>/", views.verProduto, name="detalhes"),
]
