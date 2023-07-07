from django.shortcuts import render, redirect
from comandas.models import Comanda
from produtos.models import Produto
from pedidos.models import Pedido, Pedido_Produto
# Create your views here.


def verHistorico(request):
    dsComandas = Comanda.objects.all()
    return render(request, "comandas/historico.html", {"dsComandas": dsComandas})


def verConta(request, mesa1):
    mesaContext = {'mesa': mesa1}
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
                            
        contexto = {'mesa': mesa1, 'comanda': comanda1, 'pedidos': pedidos, 'produtos': produtos}
        
        return render(request, "comandas/comandaEspera.html", contexto)
        
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

    contexto = {'mesa': mesa1, 'comanda': comanda, 'pedidos': pedidos, 'produtos': produtos,
                'verificacao': verificacao, 'verificacaoCarrinho': verificacaoCarrinho}
    pedidos = Pedido.objects.filter(comanda=comanda.cod)

    if pedidos.count() == 0:
        mesaContext = {'mesa': mesa1}
        return render(request, "pedidos/carrinhoVazio.html", mesaContext)
    else:
        return render(request, "comandas/fecharConta.html", contexto)

def fecharConta(request, id_comanda):
    # Buscar as informações e passar para o caixa ou garçom
    
        
    #
    #
    
    comanda = Comanda.objects.get(pk=id_comanda)
    mesa = comanda.mesa
    comanda.status = 1 #Em espera de pagamento
    comanda.opcaoPagamento = request.POST.get('opcoes')
    if comanda.opcaoPagamento == "Dinheiro":
        comanda.trocoPara = request.POST.get('troco')
    comanda.save()
    
    return redirect("/comandas/"+str(mesa)+"/") 
