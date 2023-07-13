from .models import Funcionario
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from funcionarios.forms import FuncionarioForm
from accounts.forms import CustomerUserForm
from django.shortcuts import render, redirect
from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from funcionarios.forms import FuncionarioForm
from funcionarios.models import Funcionario
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.shortcuts import render
import win32print
import win32api

def acesso_negado(request):
    return render(request, "funcionarios/acesso_negado.html")


class FuncionariosView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Funcionario
    template_name = 'funcionarios/index2.html'
    context_object_name = 'funcionarios'
    login_url = 'registration/login.html'

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
    funcionario = get_object_or_404(Funcionario, pk=funcionarios_id)
    user = get_object_or_404(User, pk=funcionario.user_id)
    form = CustomerUserForm(instance=user)
    formFuncionario = FuncionarioForm(instance=funcionario)
    if request.method == 'POST':
        form = CustomerUserForm(request.POST, instance=user)
        formFuncionario = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid() and formFuncionario.is_valid():
            form.save()
            formFuncionario.save()
            return HttpResponseRedirect('/funcionarios/funcionarios/')
    return render(request, "funcionarios/edit.html", {'form': form, 'formFuncionario': formFuncionario})


def remove(request, funcionarios_id):
    if not request.user.groups.filter(name='Administrador').exists():
        return redirect('acesso_negado')
    funcionarios2 = Funcionario.objects.get(pk=funcionarios_id)
    return render(request, "funcionarios/confirmRemove.html", {"funcionario": funcionarios2})


def removeFinal(request, funcionarios_id):
    funcionarios_instance = get_object_or_404(Funcionario, pk=funcionarios_id)
    if funcionarios_instance.user:
        funcionarios_instance.user.delete()
    funcionarios_instance.delete()
    return HttpResponseRedirect("/funcionarios/funcionarios/")


def register(request):
    form = CustomerUserForm()
    formFuncionario = FuncionarioForm()
    if request.method == 'POST':
        form = CustomerUserForm(request.POST)
        formFuncionario = FuncionarioForm(request.POST)
        if form.is_valid() and formFuncionario.is_valid():
            user = form.save()
            perfil = formFuncionario.save(False)
            perfil.user = user
            perfil.save()
            return HttpResponseRedirect('/funcionarios/')
    return render(request, 'registration/register.html', {'form': form, 'formFuncionario': formFuncionario})

# def listar_impressoras():
#     impressoras = win32print.EnumPrinters(
#         win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
#     print("Impressoras Disponíveis:")
#     for i, impressora in enumerate(impressoras):
#         nome_impressora = impressora[2]
#         print(f"{i+1}. {nome_impressora}")
#     opcao = int(
#         input("Ecolha uma das opções e digite o número da impressora desejada: "))
#     if opcao >= 1 and opcao <= len(impressoras):
#         return impressoras[opcao-1][2]
#     else:
#         print("Opção inválida.")
#         return None

# def definir_impressora_padrao(request):
#     impressora_atual = win32print.GetDefaultPrinter()
#     print(f"Impressora padrão atual: {impressora_atual}")
#     opcao = input("Deseja definir outra impressora como padrão? (S/N): ")
#     if opcao.lower() == "s":
#         nova_impressora = listar_impressoras()
#         if nova_impressora is not None:
#             win32print.SetDefaultPrinter(nova_impressora)
#             print(f"Impressora '{nova_impressora}' definida como padrão.")
#     else:
#         print("Nenhuma alteração realizada.")
    
#     contexto = {'nova_impressora' : nova_impressora}
#     return render(request, "pedidos/deletar.html", contexto)

def listar_impressoras():
    impressoras = win32print.EnumPrinters(
        win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
    )
    return [impressora[2] for impressora in impressoras]

def definir_impressora_padrao(request):
    impressoras = listar_impressoras()
    impressora_atual = win32print.GetDefaultPrinter()
    
    if request.method == 'POST':
        impressora_selecionada = request.POST.get('impressora_selecionada')
        if impressora_selecionada in impressoras:
            win32print.SetDefaultPrinter(impressora_selecionada)
            mensagem = f"Impressora '{impressora_selecionada}' definida como padrão."
        else:
            mensagem = "Impressora inválida."
        contexto = {'mensagem': mensagem, 'impressora_atual': impressora_atual, 'impressoras': impressoras}
        return render(request, 'funcionarios/definir_impressora_padrao.html', contexto)
    
    contexto = {'impressoras': impressoras, 'impressora_atual': impressora_atual}
    return render(request, 'funcionarios/definir_impressora_padrao.html', contexto)


