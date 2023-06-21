from comandas.models import Comanda
from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from produtos.forms import ProdutoForm, ProdutoPhotoForm
from produtos.models import Photo, Produto
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
    if request.method == "POST":
        form = ProdutoForm(request.POST)
        if form.is_valid():
            estoque = form.cleaned_data['estoque']
            if estoque >= 0:
                form.save()
                return HttpResponseRedirect('/produtos/produtos/')
            else:
                form.add_error('estoque', 'O estoque não pode ser negativo.')
    else:
        form = ProdutoForm()
    return render(request, "produtos/adicionar.html", {"form": form})


# @login_required
def editar(request, produto_cod):
    produto = Produto.objects.get(pk=produto_cod)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            estoque = form.cleaned_data['estoque']
            if estoque >= 0:
                form.save()
                return HttpResponseRedirect("/produtos/produtos/")
            else:
                form.add_error('estoque', 'O estoque não pode ser negativo.')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, "produtos/editar.html", {"form": form})


# @login_required
def remover(request, produto_cod):
    produto = Produto.objects.get(pk=produto_cod)
    return render(request, "produtos/removerFinal.html", {"produto": produto})


# @login_required
def removerFinal(request, produto_cod):
    Produto.objects.get(pk=produto_cod).delete()
    return HttpResponseRedirect("/produtos/produtos/")


# def adicionarFoto(request):
#     template_name = 'produtos/adicionar.html'
#     form = ProdutoPhotoForm(request.POST or None)

#     if request.method == 'POST':
#         # photo = request.FILES.get('photo')  # pega so um arquivo
#         #
#         photos = request.FILES.getlist('photo')  # pega vários arquivos.

#         if form.is_valid():
#             produto = form.save()

#             for photo in photos:  # Tira se for so uma
#                 Photo.objects.create(produto=produto, photo=photo)

#             # return redirect('produtos:produto_detail', produto.pk)

#             return HttpResponseRedirect("/produtos/produtos/")

#     context = {'form': form}
    # return render(request, template_name, context)


def photo_create(request):
    template_name = 'produtos/adicionar.html'
    form = ProdutoPhotoForm(request.POST or None)

    if request.method == 'POST':
        photos = request.FILES.getlist('photo')  # pega vários arquivos.
        if form.is_valid():
            produto = form.save()
            for photo in photos:
                Photo.objects.create(produto=produto, photo=photo)
            # return redirect('produtos:produto_detail', produto.cod) -> pk ou cod?

            return HttpResponseRedirect("/produtos/produtos/")
    context = {'form': form}
    return render(request, template_name, context)


# def produto_detail(request,  produto_cod):
#     template_name = 'produtos/detalhes.html'
#     obj = Produto.objects.get(pk=produto_cod)
#     context = {'object': obj}
#     return render(request, template_name, context)
