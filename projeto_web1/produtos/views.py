from django.conf import settings
import os
from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from produtos.forms import ProdutoForm
from produtos.models import Produto
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

# ------------------------------------- CARDAPIO -------------------------------------


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


# ------------------------------------- PAINEL -------------------------------------
class ProdutosView(ListView):
    model = Produto
    template_name = 'produtos/produtoList.html'
    context_object_name = 'produtos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dsProdutos'] = Produto.objects.all()
        return context


def adicionar(request):
    template_name = 'produtos/adicionar.html'
    form = ProdutoForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            estoque = form.cleaned_data['estoque']
            if estoque >= 0:
                produto = form.save()
                produto.img = request.FILES.get('img')
                produto.save()
                return HttpResponseRedirect('/produtos/produtos/')
            else:
                form.add_error('estoque', 'O estoque não pode ser negativo.')
    else:
        form = ProdutoForm()

    context = {'form': form}
    return render(request, template_name, context)

# @login_required


def editar(request, produto_cod):
    produto = Produto.objects.get(pk=produto_cod)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            estoque = form.cleaned_data['estoque']
            if estoque >= 0:
                produto = form.save(commit=False)
                if 'img' in request.FILES:
                    produto.img = request.FILES['img']
                produto.save()
                return HttpResponseRedirect('/produtos/produtos/')
            else:
                form.add_error('estoque', 'O estoque não pode ser negativo.')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produtos/editar.html', {'form': form})


# @login_required
def remover(request, produto_cod):
    produto = Produto.objects.get(pk=produto_cod)
    return render(request, "produtos/removerFinal.html", {"produto": produto})


# @login_required
# def removerFinal(request, produto_cod):
#     Produto.objects.get(pk=produto_cod).delete()
#     return HttpResponseRedirect("/produtos/produtos/")


def removerFinal(request, produto_cod):
    produto = Produto.objects.get(pk=produto_cod)

    # Excluir a imagem associada ao produto, se existir
    if produto.img:
        caminho_foto = os.path.join(settings.MEDIA_ROOT, str(produto.img))
        if os.path.exists(caminho_foto):
            os.remove(caminho_foto)

    produto.delete()
    return HttpResponseRedirect("/produtos/produtos/")
