from django.shortcuts import render
from pedidos import views
from comandas.models import Comanda
from pedidos.models import Pedido
# import Pedido

# Create your views here.
def index(request):
    
    return render(request, "garcom/index.html")

def list_pedidos(request):
    dsComanda = Comanda.objects.all() 
    
    if dsComanda.count()== 0: #verifico se não há comanda
        return render(request, "pedidos/carrinhoVazio.html") #se não tiver
    else:
        for i in dsComanda: #se tiver busco
            if i.status==0:
                comanda = Comanda.objects.get(pk=i.cod)
                
        dsPedido = Pedido.objects.filter(status=0, comanda=comanda.cod)
        if dsPedido.count()==0: #verifica se há pedido
            return render(request, "pedidos/carrinhoVazio.html")
        else: #se houver, busca ele
            for i in dsPedido:
                if i.status==0:
                    pedido = Pedido.objects.get(pk=i.cod)
    # Pedido.list_carrinho()
    
    contexto = {'dsComanda' : dsComanda, 'dsPedido': dsPedido}
    return render(request, "garcom/list_pedidos_garcon.html", contexto)
    
def fazer_pedido(request):
    # list_pedidos(request)
    
    dsComanda = Comanda.objects.all() 
    
    if dsComanda.count()== 0: #verifico se não há comanda
        return render(request, "pedidos/carrinhoVazio.html") #se não tiver
    else:
        for i in dsComanda: #se tiver busco
            if i.status==0:
                comanda = Comanda.objects.get(pk=i.cod)
                
        dsPedido = Pedido.objects.filter(status=0, comanda=comanda.cod)
        if dsPedido.count()==0: #verifica se há pedido
            return render(request, "pedidos/carrinhoVazio.html")
        else: #se houver, busca ele
            for i in dsPedido:
                if i.status==0:
                    pedido = Pedido.objects.get(pk=i.cod)
    
    contexto = {'dsComanda' : dsComanda, 'dsPedido': dsPedido}
    
    return render(request, "garcom/fazer_pedido_garcom.html", contexto)
    
