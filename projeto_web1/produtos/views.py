from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render  # IMPORTA
from django.template import loader
from produtos.forms import ProdutoForm  # IMPORTA
from produtos.models import Produto
from django.contrib.auth.decorators import login_required  # IMPORTA

# def index(request):
#     dsProdutos = Produto.objects.all()
#     return render(request, "produtos/index.html", {'dsProdutos': dsProdutos})

# def index(request):
#     dsProdutos = Produto.objects.all().exclude(estoque=0)
#     dsPratos = Produto.objects.filter(tipo__icontains="prato").exclude(estoque=0)
#     dsBebidas = Produto.objects.filter(tipo__icontains="bebida").exclude(estoque=0)
#     contexto = {'dsProdutos': dsProdutos, 'dsPratos': dsPratos, 'dsBebidas': dsBebidas}
#     return render(request, "produtos/index.html", contexto)


def index(request, mesa):
    dsPratos = Produto.objects.filter(
        tipo__icontains="prato").exclude(estoque=0)
    dsBebidas = Produto.objects.filter(
        tipo__icontains="bebida").exclude(estoque=0)
    contexto = {'mesa': mesa, 'dsPratos': dsPratos, 'dsBebidas': dsBebidas}
    return render(request, "produtos/index.html", contexto)


def listPratos(request, mesa):
    dsProdutos = Produto.objects.filter(
        tipo__icontains="prato").exclude(estoque=0)
    contexto = {
        'dsProdutos': dsProdutos,
        'mesa': mesa,
    }
    return render(request, "produtos/filtro.html", contexto)


def listBebidas(request, mesa):
    dsProdutos = Produto.objects.filter(
        tipo__icontains="bebida").exclude(estoque=0)
    contexto = {
        'dsProdutos': dsProdutos,
        'mesa': mesa,
    }
    return render(request, "produtos/filtro.html", contexto)


def verProduto(request, mesa, produto_cod):
    vProduto = Produto.objects.get(pk=produto_cod)
    dsProdutos = Produto.objects.filter(tipo__icontains=vProduto.tipo).exclude(
        estoque=0).exclude(pk=vProduto.cod)[:4]
    contexto = {'mesa': mesa, 'vProduto': vProduto, 'dsProdutos': dsProdutos}
    return render(request, "produtos/detalhes.html", contexto)


def add(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/Produto')

    else:
        form = ProdutoForm()

    return render(request, "Produto/add.html", {"form": form})
