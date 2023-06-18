from django.shortcuts import render
from pedidos.models import Pedido
from produtos.models import Produto

# Create your views here.
def adicionar(request, cod_pedido, cod_produto, quantidade):
    print("Chegou aq")
    pedido = Pedido.objets.get(pk=cod_pedido)
    produto = Produto.objects.get(pk=cod_produto)
    for a in quantidade:
        pedido.produtos+=produto
        pedido.calor+=produto.valor_unitario
    pedido.save()