from django.urls import path
from . import views

urlpatterns = [
    path("adicionar/<int:cod_pedido>/<int:cod_produto>/<int:quantidade>/", views.adicionar, name="adicionar_produtos"),
]
