from django.urls import path
from . import views
from .views import ProdutosView

# from produtos import views as v

# app_name = 'produtos'

urlpatterns = [
    
    path("", views.index, name='index'),
    
    # path('cardapio/', views.cardapio, name='cardapio'),
    
    path("cardapio/<int:produto_cod>/", views.verProduto, name="detalhes"),
    path("cardapio/pratos/", views.listPratos, name="listar_pratos"),
    path("cardapio/bebidas/", views.listBebidas, name="listar_bebidas"),

    path('produtos/', ProdutosView.as_view(), name='produtos'),

    path('produtos/add/', views.adicionar, name='adicionar'),
    path('produtos/editar/<int:produto_cod>/', views.editar, name='editar'),
    path('produtos/remover/<int:produto_cod>/', views.remover, name='remover'),
    path('produtos/remover/final/<int:produto_cod>/',
         views.removerFinal, name='removerFinal'),


    # ---------------------- Cardapio ----------------------------------------------------------------
    path("cardapio/", views.cardapio, name="cardapio"),



    # path('<int:produto_cod>/', v.produto_detail, name='produto_detail'),
]
