from django.shortcuts import redirect, render
from pedidos import views
from comandas.models import Comanda
from pedidos.models import Pedido
from pedidos.views import list_carrinho
# from projeto_web1 import produtos
from pedidos.models import Pedido_Produto
from produtos.models import Produto
# import Pedido

# Create your views here.

def list_pedidos(request):
    dsComanda = Comanda.objects.all()
              
    dsPedido = Pedido.objects.filter(status=1)
    if dsPedido.count()==0: #verifica se há pedido
        return render(request, "garcom/semPedidos.html")
    else: #se houver, busca ele
        for i in dsPedido:
            if i.status==1:
                pedido = Pedido.objects.get(pk=i.cod)
    # Pedido.list_carrinho()
    
    contexto = {'dsComanda' : dsComanda, 'dsPedido': dsPedido}
    return render(request, "garcom/list_pedidos_garcom.html", contexto)   
    
def changeStatusPedido(request, codigo_pedido):
    try:
        pedido = Pedido.objects.get(cod=codigo_pedido)
        print("Pedido: {pedido.cod} - Status: {pedido.status}")
        if pedido.status == 0 and pedido.status == 2:
            return redirect("/garcom/list_pedidos/") 
        else:
            pedido.status = 2
            pedido.save()
        contexto = {"pedido" : pedido}
        return redirect("/garcom/list_pedidos/")  
    
    except Pedido.DoesNotExist:
        # Lidar com a situação em que o pedido não existe
        return redirect("/garcom/list_pedidos/") 


def describe_pedido(request, cod_comanda, cod_pedido):
    
    pedido = Pedido.objects.get(cod=cod_pedido)
    print("Cod:  {}".format(pedido.cod))
    print("Cod: Comanda  {}".format(cod_comanda))
    
    produtosPedido = Pedido_Produto.objects.filter(
                    cod_pedido=cod_pedido)
    
    comanda = Comanda.objects.get(cod=cod_comanda)

    contexto = {'produtosPedido' : produtosPedido, "pedido" : pedido, 'comanda' : comanda}
    return render(request, "garcom/describe_pedido.html", contexto)
