from comandas.models import Comanda
from urllib3 import HTTPResponse
from produtos.models import Produto
from pedidos.models import Pedido, Pedido_Produto
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
    quantidade = int(request.POST.get('quantidade'))
    
    print(str(quantidade))
    #busco o pedido
    produto = Produto.objects.get(pk=cod_produto)
    
    produtosPedidos = Pedido_Produto.objects.filter(cod_pedido=pedido.cod, cod_produto=produto.cod)
    if produtosPedidos.count()==0: #guardo no banco se não houver daquele produto
        produtos=Pedido_Produto()
        produtos.cod_pedido=pedido
        produtos.cod_produto=produto
        produtos.quantidade=quantidade
        produtos.save()
    else:# se ja tiver, busco ele e modifico a quantidade
        for i in produtosPedidos:
            i.quantidade+=quantidade
            i.save()
    
    
    #altero os valores e estoque
    pedido.valor+=(produto.valorUnitario*int(quantidade))
    pedido.save()
    produto.estoque-=quantidade
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
        
            #pego todos os produtos do pedido
            produtosPedidos = Pedido_Produto.objects.filter(cod_pedido=pedido.cod)
            
            
            #filtragem :
            dsPratosAux = Produto.objects.filter(
                tipo__icontains="prato")#busco todos os pratos
            dsPratos=[]
            dsBebidasAux = Produto.objects.filter(
                tipo__icontains="bebida")
            dsBebidas=[]
            
            #busco os pratos
            for i in produtosPedidos:
                for a in dsPratosAux:
                    if i.cod_produto.cod==a.cod:
                        dsPratos.append(i.cod_produto)
            #busco as bebidas
            for i in produtosPedidos:
                for a in dsBebidasAux:
                    if i.cod_produto.cod==a.cod:
                        print(str(i.quantidade))
                        dsBebidas.append(i.cod_produto)
            
            
            contexto = {'mesa': mesa1, 'dsPratos': dsPratos, 'dsBebidas': dsBebidas}
            
            return render(request, "pedidos/carrinho.html", contexto)