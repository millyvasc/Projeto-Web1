from django.urls import path
from . import views
from .views import ProdutosView

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:produto_cod>/", views.verProduto, name="detalhes"),
    path("pratos/", views.listPratos, name="listar_pratos"),
    path("bebidas/", views.listBebidas, name="listar_bebidas"),

    path('produtos/', ProdutosView.as_view(), name='produtos'),
    path('produtos/add/', views.adicionar, name='adicionar'),

    path('produtos/editar/<int:produto_cod>/', views.editar, name='editar'),
    path('produtos/remover/<int:produto_cod>/', views.remover, name='remover'),
    path('produtos/remover/final/<int:produto_cod>/',
         views.removerFinal, name='removerFinal'),
]
