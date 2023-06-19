from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render  # IMPORTA
from django.template import loader
from produtos.forms import ProdutoForm  # IMPORTA
from produtos.models import Produto
from django.contrib.auth.decorators import login_required  # IMPORTA

def index(request): 
    dsProdutos = Produto.objects.all() 
    return render(request, "produtos/index.html", {'dsProdutos': dsProdutos})

# def index(request): 
#     dsPratos = Produto.objects.filter(tipo="prato").exclude(estoque=0)
#     dsBebidas = Produto.objects.filter(tipo="bebida").exclude(estoque=0)
#     contexto = {'dsPratos': dsPratos, 'dsBebidas': dsBebidas}
#     return render(request, "produtos/index.html", contexto)

def listPratos(request): 
    dsProdutos = Produto.objects.filter(tipo__icontains="prato").exclude(estoque=0)
    return render(request, "produtos/index.html", {'dsProdutos': dsProdutos})


def listBebidas(request): 
    dsProdutos = Produto.objects.filter(tipo__icontains="bebida").exclude(estoque=0)
    return render(request, "produtos/index.html", {'dsProdutos': dsProdutos})


def verProduto(request, produto_cod): 
    produto = Produto.objects.get(pk=produto_cod)
    return render(request, "produtos/detalhes.html", {"produto": produto})

def add(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST);
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/Produto')
        
    else:
        form = ProdutoForm();
    
    return render(request, "Produto/add.html", {"form": form})
