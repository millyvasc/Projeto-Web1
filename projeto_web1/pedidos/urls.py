from django.urls import path
from . import views

urlpatterns = [
    path("adicionar/<int:mesa1>/<int:cod_produto>/", views.adicionar, name="adicionar"),
    path("carrinho/", views.list_orders, name="list_orders"),
    #path("<int:produto_cod>/", views.verProduto, name="detalhes"),
]
