from datetime import date
from datetime import datetime
from django.shortcuts import render, redirect
from comandas.models import Comanda
from produtos.models import Produto
from pedidos.models import Pedido, Pedido_Produto


def pedidosFechamento(request):
    comandas = Comanda.objects.filter(status=1).order_by("data_e_hora")
    
    contexto ={'dsComandas': comandas}
    return render(request, "comandas/pedidosFechamento.html", contexto)

def pedidosFechamentoConcluir(request, cod_comanda):
    comanda = Comanda.objects.get(pk=cod_comanda)
    comanda.status=2
    comanda.save()
    
    return redirect("/comandas/comandas/")


def verHistorico(request):
    if not request.user.groups.filter(name__in=['Administrador', 'Caixa']).exists():
        return redirect('acesso_negado')

    filtro = None
    if request.method == 'POST':
        filtro = request.POST.get('filtro')

    dataAtual = date.today()

    if filtro == '1':
        dsComandas = Comanda.objects.filter(
            data_e_hora__date=dataAtual, status=0)
    elif filtro == '2':
        dsComandas = Comanda.objects.filter(
            data_e_hora__date=dataAtual, status=1)
    elif filtro == '3':
        dsComandas = Comanda.objects.filter(
            data_e_hora__date=dataAtual, status=2)
    elif filtro == '4':
        mesaInput = request.POST.get('mesa')
        dsComandas = Comanda.objects.filter(
            data_e_hora__date=dataAtual, mesa=mesaInput)
    else:
        dsComandas = Comanda.objects.filter(data_e_hora__date=dataAtual)

    lucroDiario = 0
    for comanda in dsComandas:
        lucroDiario += comanda.valorTotal

    contexto = {
        "dsComandas": dsComandas,
        "lucroDiario": lucroDiario,
        "filtro": filtro,
    }

    return render(request, "comandas/historico.html", contexto)


def verHistoricoCompleto(request):
    if not request.user.groups.filter(name='Administrador').exists():
        return redirect('acesso_negado')

    filtro = None
    if request.method == 'POST':
        filtro = request.POST.get('filtro')

    if filtro == '1':
        dsComandas = Comanda.objects.filter(status=0)
    elif filtro == '2':
        dsComandas = Comanda.objects.filter(status=1)
    elif filtro == '3':
        dsComandas = Comanda.objects.filter(status=2)
    elif filtro == '4':
        mesaInput = request.POST.get('mesa')
        dsComandas = Comanda.objects.filter(mesa=mesaInput)
    else:
        dsComandas = Comanda.objects.all()

    lucroDiario = 0
    for comanda in dsComandas:
        lucroDiario += comanda.valorTotal

    contexto = {
        "dsComandas": dsComandas,
        "lucroDiario": lucroDiario,
        "filtro": filtro,
    }

    return render(request, "comandas/historicoAll.html", contexto)


def detalharComanda(request, cod_comanda):
    comanda = Comanda.objects.get(cod=cod_comanda)
    dsPedidos = Pedido.objects.filter(comanda=comanda)
    produtosAux = Produto.objects.all()
    produtos = []

    for pedido in dsPedidos:
        produtosPedidos = Pedido_Produto.objects.filter(cod_pedido=pedido)

        for i in produtosPedidos:
            for a in produtosAux:
                if i.cod_produto.cod == a.cod:
                    i.cod_produto.valorUnitario = (
                        a.valorUnitario*i.quantidade)
                    i.cod_produto.estoque = i.quantidade
                    i.cod_produto.cod = pedido.cod
                    produtos.append(i.cod_produto)

    contexto = {
        "comanda": comanda,
        "dsPedidos": dsPedidos,
        "produtos": produtos
    }

    return render(request, "comandas/detalhar.html", contexto)


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
                    'pedidos': pedidos, 'produtos': produtos}

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
    comanda.status = 1  # Em espera de pagamento
    comanda.opcaoPagamento = request.POST.get('opcoes')
    if comanda.opcaoPagamento == "Dinheiro":
        comanda.troco = float(request.POST.get('troco'))
        comanda.troco-=float(comanda.valorTotal)

    nova_data_e_hora = datetime.now()
    comanda.data_e_hora = nova_data_e_hora
    comanda.save()

    return redirect("/comandas/"+str(mesa)+"/")
