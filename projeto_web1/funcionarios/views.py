from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render  # IMPORTA
from django.template import loader
from funcionarios.forms import FuncionarioForm  # IMPORTA
from funcionarios.models import Funcionario
from django.contrib.auth.decorators import login_required  # IMPORTA


from django.views.generic import ListView
from produtos.models import Produto

class ProdutosView(ListView):
    model = Produto
    template_name = 'produtos/index.html'
    context_object_name = 'produtos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produtos'] = Produto.objects.all()
        return context



def index(request): 
    dsFuncionarios = Funcionario.objects.all() 
    return render(request, "funcionarios/index.html", {'dsFuncionarios': dsFuncionarios})



def add(request):
    if request.method == "POST":
        form = FuncionarioForm(request.POST);
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/Funcionario')
        
    else:
        form = FuncionarioForm();
    
    return render(request, "Funcionario/add.html", {"form": form})
