from django.shortcuts import render
from pedidos import views
from comandas.models import Comanda
from pedidos.models import Pedido
from pedidos.views import list_carrinho
# from projeto_web1 import produtos
from pedidos.models import Pedido_Produto
from produtos.models import Produto
# import Pedido

# Create your views here.
def index(request):
    
    return render(request, "garcom/index.html")

def list_mesas(request):
    dsComanda = Comanda.objects.all() 
    
    if dsComanda.count()== 0: #verifico se não há comanda
        return render(request, "pedidos/carrinhoVazio.html") #se não tiver
    else:
        for i in dsComanda: #se tiver busco
            if i.status==0:
                comanda = Comanda.objects.get(pk=i.cod)
                
        dsPedido = Pedido.objects.filter(status=1, comanda=comanda.cod)
        if dsPedido.count()==0: #verifica se há pedido
            return render(request, "pedidos/carrinhoVazio.html")
        else: #se houver, busca ele
            for i in dsPedido:
                if i.status==1:
                    pedido = Pedido.objects.get(pk=i.cod)
    # Pedido.list_carrinho()
    
    contexto = {'dsComanda' : dsComanda, 'dsPedido': dsPedido}
    return render(request, "garcom/list_mesas_garcon.html", contexto)

def list_pedidos(request, mesa1):
    
    # # list_carrinho(request, mesa1)
    # dsComanda = Comanda.objects.filter(status=0, mesa=mesa1) 
    # if dsComanda.count()== 0: #verifico se não há comanda
    #     return render(request, "pedidos/carrinhoVazio.html") #se não tiver
    # else:
    #     for i in dsComanda: #se tiver busco
    #         if i.status==0:
    #             comanda = Comanda.objects.get(pk=i.cod)
        
    #     dsPedido = Pedido.objects.filter(status=1, comanda=comanda.cod)
    #     if dsPedido.count()==0: #verifico se há pedidp
    #         return render(request, "pedidos/carrinhoVazio.html")
    #     else: #se houver, busca ele
    #         for i in dsPedido:
    #             if i.status==1:
    #                 pedido = Pedido.objects.get(pk=i.cod)
        
    #         # #pego todos os produtos do pedido
    #         produtosPedido = Pedido_Produto.objects.filter(cod_pedido=pedido.cod)
            
            
    #         # #filtragem :
    #         # dsPratosAux = Produto.objects.filter(
    #         #     tipo__icontains="prato")#busco todos os pratos
    #         # dsPratos=[]
    #         # dsBebidasAux = Produto.objects.filter(
    #         #     tipo__icontains="bebida")
    #         # dsBebidas=[]
            
    #         # #busco os pratos
    #         # for i in produtosPedidos:
    #         #     for a in dsPratosAux:
    #         #         if i.cod_produto.cod==a.cod:
    #         #             i.cod_produto.estoque=i.quantidade
    #         #             dsPratos.append(i.cod_produto)
    #         # #busco as bebidas
    #         # for i in produtosPedidos:
    #         #     for a in dsBebidasAux:
    #         #         if i.cod_produto.cod==a.cod:
    #         #             i.cod_produto.estoque=i.quantidade
    #         #             dsBebidas.append(i.cod_produto)
            
            
    #         contexto = {'mesa': mesa1, 'dsPedido' : dsPedido, 'comanda': comanda, 'produtosPedido' : produtosPedido }
            
    #         return render(request, "garcom/list_pedidos_mesa.html", contexto)
    mesaContext = {'mesa' : mesa1}
    dsComanda = Comanda.objects.filter(status=0, mesa=mesa1)
    if dsComanda.count() == 0:  # verifico se não há comanda
        # se não tiver

        dsComanda1 = Comanda.objects.filter(status=1, mesa=mesa1)
        if dsComanda1.count() == 0:
            return render(request, "pedidos/carrinhoVazio.html", mesaContext)
        else:
            for i in dsComanda1:  # se tiver busco
                comanda1 = i
            pedidos = Pedido.objects.filter(comanda=comanda1.cod)
            produtosAux = Produto.objects.all()
            produtos = []
            # busco todos os produtos de todos os pedidos
            for p in pedidos:
                produtosPedidos = Pedido_Produto.objects.filter(
                    cod_pedido=p.cod)
                for i in produtosPedidos:
                    for a in produtosAux:
                        if i.cod_produto.cod == a.cod:  # salvo os produtoos, mas antes
                            # mudo o valorUnitario para a soma de todos os produtos iguais
                            i.cod_produto.valorUnitario = (
                                a.valorUnitario*i.quantidade)
                            # 'salvo' a quantidade de produtos do pedido no estoque do produto
                            i.cod_produto.estoque = i.quantidade
                            i.cod_produto.cod = p.cod  # 'salvo' o id do pedido no id do produto
                            # isso tudo é apenas para a visualização no html, pois não modifico o produto no BD
                            produtos.append(i.cod_produto)

        contexto = {'mesa': mesa1, 'comanda': comanda1,
                    'dsPedido': pedidos, 'produtosPedido': produtos}
        # contexto = {'mesa': mesa1, 'dsPedido' : dsPedido, 'comanda': comanda, 'produtosPedido' : produtosPedido }
        return render(request, "garcom/list_pedidos_mesa.html", contexto)

    else:
        for i in dsComanda:  # se tiver busco
            comanda = i

    pedidos = Pedido.objects.filter(comanda=comanda.cod)
    produtosAux = Produto.objects.all()
    produtos = []
    # busco todos os produtos de todos os pedidos
    verificacao = 0
    verificacaoCarrinho = 0
    for p in pedidos:
        if p.status != 2:  # verifico se os pedidos estão todos concluidos
            verificacao = verificacao + 1
        if p.status == 0:  # olho se tem carrinho aberto
            verificacaoCarrinho = verificacaoCarrinho + 1

        produtosPedidos = Pedido_Produto.objects.filter(cod_pedido=p.cod)

        for i in produtosPedidos:
            for a in produtosAux:
                if i.cod_produto.cod == a.cod:  # salvo os produtoos, mas antes
                    # mudo o valorUnitario para a soma de todos os produtos iguais
                    i.cod_produto.valorUnitario = (
                        a.valorUnitario*i.quantidade)
                    # 'salvo' a quantidade de produtos do pedido no estoque do produto
                    i.cod_produto.estoque = i.quantidade
                    i.cod_produto.cod = p.cod  # 'salvo' o id do pedido no id do produto
                    # isso tudo é apenas para a visualização no html, pois não modifico o produto no BD
                    produtos.append(i.cod_produto)

    contexto = {'mesa': mesa1, 'comanda': comanda, 'dsPedido': pedidos, 'produtosPedido': produtos,
                'verificacao': verificacao, 'verificacaoCarrinho': verificacaoCarrinho}
    pedidos = Pedido.objects.filter(comanda=comanda.cod)

    if pedidos.count() == 0:
        mesaContext = {'mesa': mesa1}
        return render(request, "pedidos/carrinhoVazio.html", mesaContext)
    else:
        # return render(request, "comandas/fecharConta.html", contexto)
        return render(request, "garcom/list_pedidos_mesa.html", contexto)
    
    
def changeStatusPedido(request, codigo_pedido):
    try:
        pedido = Pedido.objects.get(cod=codigo_pedido)
        print("Pedido: {pedido.cod} - Status: {pedido.status}")
        if pedido.status == 0 and pedido.status == 2:
            return render(request, "garcom/list_pedidos_mesa.html", contexto)
        else:
            pedido.status = 2
            pedido.save()
        contexto = {"pedido" : pedido}
    
        return render(request, "garcom/list_pedidos_mesa.html", contexto)
    
    except Pedido.DoesNotExist:
        # Lidar com a situação em que o pedido não existe
        return render(request, "garcom/pedido_nao_encontrado.html")

def list_pedido(request, mesa1):
    # list_carrinho(request, mesa1)
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
                        i.cod_produto.estoque=i.quantidade
                        dsPratos.append(i.cod_produto)
            #busco as bebidas
            for i in produtosPedidos:
                for a in dsBebidasAux:
                    if i.cod_produto.cod==a.cod:
                        i.cod_produto.estoque=i.quantidade
                        dsBebidas.append(i.cod_produto)
            
            
            contexto = {'mesa': mesa1, 'dsPratos': dsPratos, 'dsBebidas': dsBebidas, 'pedido' : pedido }
            
            return render(request, "garcom/list_pedido.html", contexto)
    
def fazer_pedido(request):
    # list_pedidos(request)
    
    dsComanda = Comanda.objects.all() 
    
    if dsComanda.count()== 0: #verifico se não há comanda
        return render(request, "pedidos/carrinhoVazio.html") #se não tiver
    else:
        for i in dsComanda: #se tiver busco
            if i.status==0:
                comanda = Comanda.objects.get(pk=i.cod)
                
        dsPedido = Pedido.objects.filter(status=0, comanda=comanda.cod)
        if dsPedido.count()==0: #verifica se há pedido
            return render(request, "pedidos/carrinhoVazio.html")
        else: #se houver, busca ele
            for i in dsPedido:
                if i.status==0:
                    pedido = Pedido.objects.get(pk=i.cod)
    
    contexto = {'dsComanda' : dsComanda, 'dsPedido': dsPedido}
    
    return render(request, "garcom/fazer_pedido_garcom.html", contexto)
    
