from django.urls import path
from . import views

urlpatterns = [
    path("adicionar/<int:mesa1>/<int:cod_produto>/", views.adicionar, name="adicionar"),
    path("<int:mesa1>/carrinho/", views.list_carrinho, name="list_carrinho"),
    #path("<int:produto_cod>/", views.verProduto, name="detalhes"),
]
