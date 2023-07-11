from django.shortcuts import render
from pedidos import views
from comandas.models import Comanda
from pedidos.models import Pedido
from pedidos.views import list_carrinho
from pedidos.models import Pedido_Produto
from produtos.models import Produto


def index(request):
    return render(request, "garcom/index.html")


def list_mesas(request):
    dsComanda = Comanda.objects.all()
    if dsComanda.count() == 0:
        return render(request, "pedidos/carrinhoVazio.html")
    else:
        for i in dsComanda:
            if i.status == 0:
                comanda = Comanda.objects.get(pk=i.cod)

        dsPedido = Pedido.objects.filter(status=0, comanda=comanda.cod)
        if dsPedido.count() == 0:
            return render(request, "pedidos/carrinhoVazio.html")
        else:
            for i in dsPedido:
                if i.status == 0:
                    pedido = Pedido.objects.get(pk=i.cod)
    contexto = {'dsComanda': dsComanda, 'dsPedido': dsPedido}
    return render(request, "garcom/list_mesas_garcon.html", contexto)


def list_pedidos(request, mesa1):
    dsComanda = Comanda.objects.filter(status=0, mesa=mesa1)
    if dsComanda.count() == 0:
        return render(request, "pedidos/carrinhoVazio.html")
    else:
        for i in dsComanda:
            if i.status == 0:
                comanda = Comanda.objects.get(pk=i.cod)
        dsPedido = Pedido.objects.filter(status=0, comanda=comanda.cod)
        if dsPedido.count() == 0:
            return render(request, "pedidos/carrinhoVazio.html")
        else:
            for i in dsPedido:
                if i.status == 0:
                    pedido = Pedido.objects.get(pk=i.cod)
            contexto = {'mesa': mesa1,
                        'dsPedido': dsPedido, 'comanda': comanda}
            return render(request, "garcom/list_pedidos_mesa.html", contexto)


def list_pedido(request, mesa1):
    dsComanda = Comanda.objects.filter(status=0, mesa=mesa1)
    if dsComanda.count() == 0:
        return render(request, "pedidos/carrinhoVazio.html")
    else:
        for i in dsComanda:
            if i.status == 0:
                comanda = Comanda.objects.get(pk=i.cod)
        dsPedido = Pedido.objects.filter(status=0, comanda=comanda.cod)
        if dsPedido.count() == 0:
            return render(request, "pedidos/carrinhoVazio.html")
        else:
            for i in dsPedido:
                if i.status == 0:
                    pedido = Pedido.objects.get(pk=i.cod)
            produtosPedidos = Pedido_Produto.objects.filter(
                cod_pedido=pedido.cod)
            dsPratosAux = Produto.objects.filter(
                tipo__icontains="prato")
            dsPratos = []
            dsBebidasAux = Produto.objects.filter(
                tipo__icontains="bebida")
            dsBebidas = []
            for i in produtosPedidos:
                for a in dsPratosAux:
                    if i.cod_produto.cod == a.cod:
                        i.cod_produto.estoque = i.quantidade
                        dsPratos.append(i.cod_produto)
            for i in produtosPedidos:
                for a in dsBebidasAux:
                    if i.cod_produto.cod == a.cod:
                        i.cod_produto.estoque = i.quantidade
                        dsBebidas.append(i.cod_produto)
            contexto = {'mesa': mesa1, 'dsPratos': dsPratos,
                        'dsBebidas': dsBebidas, 'pedido': pedido}
            return render(request, "garcom/list_pedido.html", contexto)


def fazer_pedido(request):
    dsComanda = Comanda.objects.all()
    if dsComanda.count() == 0:
        return render(request, "pedidos/carrinhoVazio.html")
    else:
        for i in dsComanda:
            if i.status == 0:
                comanda = Comanda.objects.get(pk=i.cod)
        dsPedido = Pedido.objects.filter(status=0, comanda=comanda.cod)
        if dsPedido.count() == 0:
            return render(request, "pedidos/carrinhoVazio.html")
        else:
            for i in dsPedido:
                if i.status == 0:
                    pedido = Pedido.objects.get(pk=i.cod)
    contexto = {'dsComanda': dsComanda, 'dsPedido': dsPedido}
    return render(request, "garcom/fazer_pedido_garcom.html", contexto)
