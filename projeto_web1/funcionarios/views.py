from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render  # IMPORTA
from django.template import loader
from funcionarios.forms import FuncionarioForm  # IMPORTA
from funcionarios.models import Funcionario
from django.contrib.auth.decorators import login_required  # IMPORTA
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView
from produtos.models import Produto



class FuncionariosView(LoginRequiredMixin,ListView):
    model = Funcionario
    template_name = 'funcionarios/index2.html'
    context_object_name = 'funcionarios'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dsFuncionarios'] = Funcionario.objects.all()
        return context

@login_required
def index2(request):
    dsFuncionarios = Funcionario.objects.all()
    return render(request, "funcionarios/index2.html", {'dsFuncionarios': dsFuncionarios})


@login_required

def add(request):
    
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/funcionarios/')
        
    else:
        form = FuncionarioForm()

    return render(request, 'funcionarios/add.html', {"form":form})


from accounts.forms import CustomerUserForm
from funcionarios.forms import FuncionarioForm

def edit(request, funcionarios_id=None):
    perfil = None

    if funcionarios_id:
        perfil = get_object_or_404(Funcionario, id=funcionarios_id)

    if request.method == 'POST':
        form = CustomerUserForm(request.POST, instance=perfil.user if perfil else None)

        if form.is_valid():
            user = form.save()  # Salva o usuário atualizado
            if perfil:
                perfil.cpf = form.cleaned_data['cpf']
                perfil.telefone = form.cleaned_data['telefone']
                perfil.endereco = form.cleaned_data['endereco']
                perfil.save()  # Atualiza a instância de funcionarios associada ao usuário
            else:
                perfil = Funcionario(user=user, cpf=form.cleaned_data['cpf'], telefone=form.cleaned_data['telefone'], endereco=form.cleaned_data['endereco'])
                perfil.save()  # Cria uma nova instância de funcionarios associada ao usuário
            return HttpResponseRedirect('/funcionarios/')
    else:
        form = CustomerUserForm(instance=perfil.user if perfil else None)

    context = {
        'form': form,
        'funcionarios_id': funcionarios_id
    }

    return render(request, 'funcionarios/edit.html', context)




#@login_required
#@user_passes_test(lambda user: user.groups.filter(name='Funcionarios').exists())
def remove(request, funcionarios_id):
    
    funcionarios2 = Funcionario.objects.get(pk=funcionarios_id)
    
    return render(request, "funcionarios/confirmRemove.html", {"funcionario" : funcionarios2})


#def removeFinal(request, funcionarios_id):
    
    funcionarios.objects.get(pk=funcionarios_id).delete()
    
    return HttpResponseRedirect("/funcionarios/")




def removeFinal(request, funcionarios_id):
    funcionarios_instance = get_object_or_404(Funcionario, pk=funcionarios_id)

    # Excluir o usuário associado
    if funcionarios_instance.user:
        funcionarios_instance.user.delete()

    # Excluir a instância de funcionarios
    funcionarios_instance.delete()

    return HttpResponseRedirect("/funcionarios/")




def register(request):
    form = CustomerUserForm()
    if request.method == 'POST':
        form = CustomerUserForm(request.POST)
        if form.is_valid():
            user = form.save()  # Salva o novo usuário
            perfil = Funcionario(user=user, cpf=form.cleaned_data['cpf'], telefone=form.cleaned_data['telefone'], endereco=form.cleaned_data['endereco'])
            perfil.save()  # Cria uma nova instância de PerfilUsuario associada ao usuário
            return HttpResponseRedirect('/funcionarios/')
    else:
        form = CustomerUserForm()
        
    return render(request, 'registration/register.html', {'form': form})


