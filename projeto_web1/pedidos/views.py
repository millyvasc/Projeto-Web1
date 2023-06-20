from comandas.models import Comanda
from urllib3 import HTTPResponse
from produtos.models import Produto
from pedidos.models import Pedido
from django.shortcuts import redirect, render

def adicionar(request, mesa1, cod_produto):
    
    #se não houver comanda aberta na mesa, abre
    dsComanda = Comanda.objects.filter(status=0, mesa=mesa1) 
    #dsComandaTamanho = 
    if dsComanda.count()== 0:
        comanda = Comanda()
        comanda.mesa=mesa1
        comanda.save()
    #busco a comanda da mesa que esta em aberto (status=0)
    else:
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

# Método para listar todos o carrinho
def list_carrinho(request, mesa1):
    
    dsComanda = Comanda.objects.filter(status=0, mesa=mesa1) 
    if dsComanda.count()== 0: #verifico se não há comanda
        return render(request, "pedidos/carrinhoVazio.html") #se não tiver
    else:
        for i in dsComanda: #se tiver busco
            if i.status==0:
                comanda = Comanda.objects.get(pk=i.cod)
        
        dsPedido = Pedido.objects.filter(status=0, comanda=comanda.cod)
        if dsPedido.count()==0: #verifico se há pedidp
            return render(request, "pedidos/carrinhoVazio.html")
        else: #se houver, busca ele
            for i in dsPedido:
                if i.status==0:
                    pedido = Pedido.objects.get(pk=i.cod)
        
            produtos = pedido.produtos.all() #pego todos os produtos do pedido
            
            #filtragem de apenas pratos
            dsPratosAux = Produto.objects.filter(
                tipo__icontains="prato")#busco todos os pratos
            dsPratos=[]
            for i in produtos:
                for a in dsPratosAux:
                    if i.cod==a.cod: #se um produto do pedido for prato adiciona
                        dsPratos.append(i)
            #filtragem de apenas pedidos     
            dsBebidasAux = Produto.objects.filter(
                tipo__icontains="bebida")
            dsBebidas=[]
            for i in produtos:
                for a in dsBebidasAux:
                    if i.cod==a.cod:
                        dsBebidas.append(i)
            
            contexto = {'mesa': mesa1, 'dsPratos': dsPratos, 'dsBebidas': dsBebidas}
            
            return render(request, "pedidos/carrinho.html", contexto)