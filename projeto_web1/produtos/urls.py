from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:produto_cod>/", views.verProduto, name="detalhes"),
    path("pratos/", views.listPratos, name="listar_pratos"),
    path("bebidas/", views.listBebidas, name="listar_bebidas"),
]

