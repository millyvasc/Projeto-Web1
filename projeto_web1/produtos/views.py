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



def add(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST);
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/Produto')
        
    else:
        form = ProdutoForm();
    
    return render(request, "Produto/add.html", {"form": form})
