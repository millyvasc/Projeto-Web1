from django.shortcuts import render

# Create your views here.


def verHistorico(request):

    # contexto = {'mesa': mesa, 'vProduto': vProduto, 'dsProdutos': dsProdutos}
    return render(request, "comandas/historico.html")
