from .models import Funcionario
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from funcionarios.forms import FuncionarioForm
from accounts.forms import CustomerUserForm
from django.shortcuts import render, redirect
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
from django.contrib.auth.models import User, Group
from django.shortcuts import render


def acesso_negado(request):
    return render(request, "funcionarios/acesso_negado.html")


class FuncionariosView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Funcionario
    template_name = 'funcionarios/index2.html'
    context_object_name = 'funcionarios'
    login_url = 'registration/login.html'  # Defina a URL de login adequada
      # Mensagem de acesso negado

    def test_func(self):
        return self.request.user.groups.filter(name='Administrador').exists()

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:

            return redirect('acesso_negado')
        return HttpResponse(render(self.request, 'funcionarios/menssagemLogin.html'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dsFuncionarios'] = Funcionario.objects.all()
        return context

@login_required
def index2(request):
    

    
    return render(request, "funcionarios/index.html")


@login_required
def add(request):

    if request.method == 'POST':
        form = FuncionarioForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/funcionarios/')

    else:
        form = FuncionarioForm()

    return render(request, 'funcionarios/add.html', {"form": form})


def edit(request,  funcionarios_id):
    # Obtém o usuário existente
    # Obtém o perfil do usuário que é o Funcionário existente
    funcionario = get_object_or_404(Funcionario, pk=funcionarios_id)
    user = get_object_or_404(User, pk=funcionario.user_id)

    form = CustomerUserForm(instance=user)
    formFuncionario = FuncionarioForm(instance=funcionario)

    if request.method == 'POST':
        form = CustomerUserForm(request.POST, instance=user)
        formFuncionario = FuncionarioForm(request.POST, instance=funcionario)

        if form.is_valid() and formFuncionario.is_valid():
            form.save()  # Salva as alterações do usuário
            formFuncionario.save()  # Salva as alterações do perfil
            return HttpResponseRedirect('/funcionarios/funcionarios/')

    return render(request, "funcionarios/edit.html", {'form': form, 'formFuncionario': formFuncionario})


def remove(request, funcionarios_id):
    if not request.user.groups.filter(name='Administrador').exists():
        return redirect('acesso_negado')

    funcionarios2 = Funcionario.objects.get(pk=funcionarios_id)
    return render(request, "funcionarios/confirmRemove.html", {"funcionario": funcionarios2})


# def removeFinal(request, funcionarios_id):

    funcionarios.objects.get(pk=funcionarios_id).delete()

    return HttpResponseRedirect("/funcionarios/")


def removeFinal(request, funcionarios_id):
    funcionarios_instance = get_object_or_404(Funcionario, pk=funcionarios_id)

    # Excluir o usuário associado
    if funcionarios_instance.user:
        funcionarios_instance.user.delete()

    # Excluir a instância de funcionarios
    funcionarios_instance.delete()

    return HttpResponseRedirect("/funcionarios/funcionarios/")


def register(request):
    form = CustomerUserForm()
    formFuncionario = FuncionarioForm()
    if request.method == 'POST':
        form = CustomerUserForm(request.POST)
        formFuncionario = FuncionarioForm(request.POST)
        if form.is_valid() and formFuncionario.is_valid():
            user = form.save()  # Salva o novo usuário
            perfil = formFuncionario.save(False)
            perfil.user = user
            perfil.save()  # Cria uma nova instância de PerfilUsuario associada ao usuário
            return HttpResponseRedirect('/funcionarios/')

    return render(request, 'registration/register.html', {'form': form, 'formFuncionario': formFuncionario})

