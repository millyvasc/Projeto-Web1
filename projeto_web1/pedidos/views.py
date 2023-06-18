from django.shortcuts import redirect, render
from pedidos.models import Pedido
from produtos.models import Produto

# Create your views here.
def adicionar(mesa, cod_pedido, cod_produto, quantidade): 
    print("Chegou aq")
    pedido = Pedido.objects.get(pk=cod_pedido) #busca o pedido e o produto pelo codigo.
    produto = Produto.objects.get(pk=cod_produto)
    for a in range(quantidade):  #faz uma repetição que adiciona o produto a quantidade desejada e ja altera o valor
        pedido.produtos.add(produto)
        pedido.valor=int(pedido.valor)+int(produto.valorUnitario)
    
    pedido.save()   #Salvo esses produtos do pedido no banco
    return redirect("/cardapio/") #volto para o pardapio
    #return render(request, "cardapio.html")