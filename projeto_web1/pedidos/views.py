from comandas.models import Comanda
from urllib3 import HTTPResponse
from produtos.models import Produto
from pedidos.models import Pedido
from django.shortcuts import redirect, render

def adicionar(request, mesa1, cod_produto):
    
    
    
    #busco a comanda da mesa que esta em aberto (status=0)
    dsComanda = Comanda.objects.filter(status=0, mesa=mesa1)
    for i in dsComanda:
        if i.status==0:
            comanda = Comanda.objects.get(pk=i.cod)
    
    #busco o pedido em aberto daquela comanda
    dsPedido = Pedido.objects.filter(status=0, comanda=comanda.cod)
    
    dsPedidoTamanho = dsPedido.count() #pego o numero de itens no dsPedido
    
    if dsPedidoTamanho==0: #se não houver pedido em andamento cria um
        pedido = Pedido()
        pedido.comanda=comanda
        pedido.save()
    else: #se houver, busca ele
        for i in dsPedido:
            if i.status==0:
                pedido = Pedido.objects.get(pk=i.cod)
    
    
    #pego a quantidade do form
    quantidade = request.POST.get('quantidade')
    
    print(str(quantidade))
    #busco o pedido
    produto = Produto.objects.get(pk=cod_produto)
    
    #adiciono n vezes o produto em pedido
    for a in range(int(quantidade)):
        pedido.produtos.add(produto)
        pedido.valor+=produto.valorUnitario #ja altero o valor
    pedido.save()#salvo as modificações
    produto.estoque-=int(quantidade)#baixa no escoque
    produto.save()
    
    return redirect("/"+str(mesa1)+"/cardapio/") #retorno pro cardapio

# Método para listar todos os pedidos da mesa
def list_orders(request, mesa1):
    # dsProducts = Produto.objects.get()
    
    return redirect("/"+str(mesa1)+"/carrinho/")
    