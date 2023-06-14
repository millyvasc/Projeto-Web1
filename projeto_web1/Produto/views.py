from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render  # IMPORTA
from django.template import loader
from Produto.forms import ProdutoForm  # IMPORTA
from Produto.models import Pessoas






def add(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST);
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/Produto')
        
    else:
        form = ProdutoForm();
    
    return render(request, "Produto/add.html", {"form": form})
