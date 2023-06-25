from comandas.models import Comanda
from produtos.models import Produto
from pedidos.models import Pedido, Pedido_Produto
from django.shortcuts import redirect, render

#----------------------------------------------> Carrinho <----------------------------------------------
def adicionar(request, mesa1, cod_produto):
    #crio ou busco a comanda
    dsComanda = Comanda.objects.filter(status=0, mesa=mesa1) 
    if dsComanda.count()== 0:
        comanda = Comanda()
        comanda.mesa=mesa1
        comanda.save()
    else:
        for i in dsComanda:
            if i.status==0:
                comanda = Comanda.objects.get(pk=i.cod)
    
    #busco o pedido em aberto daquela comanda
    dsPedido = Pedido.objects.filter(status=0, comanda=comanda.cod)
    if dsPedido.count()==0: #se não houver pedido em andamento cria um
        pedido = Pedido()
        pedido.comanda=comanda
        pedido.save()
    else: #se houver, busca ele
        for i in dsPedido:
            if i.status==0:
                pedido = Pedido.objects.get(pk=i.cod)
    
    #pego a quantidade do form
    quantidade = int(request.POST.get('quantidade'))
    
    #busco o pedido
    produto = Produto.objects.get(pk=cod_produto)
    
    #salvo o produto no "pedido"
    produtosPedidos = Pedido_Produto.objects.filter(cod_pedido=pedido.cod, cod_produto=produto.cod)
    if produtosPedidos.count()==0: #guardo no banco se não houver daquele produto
        produtos=Pedido_Produto()
        produtos.cod_pedido=pedido
        produtos.cod_produto=produto
        produtos.quantidade=quantidade
        produtos.save()
    else:# se ja tiver, busco ele e modifico a quantidade
        for i in produtosPedidos:
            i.quantidade+=quantidade
            i.save()
    
    #altero os valores e estoque
    pedido.valor+=(produto.valorUnitario*quantidade)
    pedido.save()
    produto.estoque-=quantidade
    produto.save()
    
    return redirect("/"+str(mesa1)+"/cardapio/") #retorno pro cardapio

# Método para listar todos o carrinho
def list_carrinho(request, mesa1):
    mesaContext={'mesa': mesa1}
    dsComanda = Comanda.objects.filter(status=0, mesa=mesa1) 
    if dsComanda.count()== 0: #verifico se não há comanda
        return render(request, "pedidos/carrinhoVazio.html", mesaContext) #se não tiver
    else:
        for i in dsComanda: #se tiver busco
            if i.status==0:
                comanda = Comanda.objects.get(pk=i.cod)
        
        dsPedido = Pedido.objects.filter(status=0, comanda=comanda.cod)
        if dsPedido.count()==0: #verifico se há pedidp
            return render(request, "pedidos/carrinhoVazio.html", mesaContext)
        else: #se houver, busca ele
            for i in dsPedido:
                if i.status==0:
                    pedido = Pedido.objects.get(pk=i.cod)

            
            produtosPedidos = Pedido_Produto.objects.filter(cod_pedido=pedido.cod)
            #Verifico se há produtos no pedido
            if produtosPedidos.count()==0:
                return render(request, "pedidos/carrinhoVazio.html", mesaContext)
            else:
                #filtragem :
                dsPratosAux = Produto.objects.filter(tipo__icontains="prato")
                dsPratos=[]
                dsBebidasAux = Produto.objects.filter(tipo__icontains="bebida")
                dsBebidas=[]
            
                soma=0 #guardo o valor total do pedido
                for i in produtosPedidos:
                    for a in dsPratosAux: #guardo os pratos
                        if i.cod_produto.cod==a.cod:
                            i.cod_produto.estoque=i.quantidade
                            dsPratos.append(i.cod_produto)
                            soma=soma+(a.valorUnitario*i.quantidade)
                    for a in dsBebidasAux: #guardo as bebidas
                        if i.cod_produto.cod==a.cod:
                            i.cod_produto.estoque=i.quantidade
                            dsBebidas.append(i.cod_produto)
                            soma=soma+(a.valorUnitario*i.quantidade)
                
                contexto = {'mesa': mesa1, 'dsPratos': dsPratos, 'dsBebidas': dsBebidas, 'soma': soma}
                return render(request, "pedidos/carrinho.html", contexto)
        
#Método para remover algo do carrinho
def remover_carrinho(request, mesa1, cod_produto):
    pedido = buscarPedidoAberto(request, mesa1)
    vProduto = Produto.objects.get(pk=cod_produto)
    produto=Pedido_Produto.objects.filter(cod_pedido=pedido.cod, cod_produto=vProduto.cod)
    #altero os valores de estoque dos produtos, para a quantidade do produto no pedido
    for i in produto:
        if i.cod_produto.cod==vProduto.cod:
            vProduto.estoque=i.quantidade
    
    contexto = {'mesa': mesa1, 'vProduto': vProduto}
    return render(request, "pedidos/carrinhoRemover.html", contexto)

#Método que confirma a remoção
def remover_carrinho_confirmar(request, mesa1, cod_produto):
    #Busco a quantidade a se remover
    quantidadeDeletar = int(request.POST.get('quantidade'))
    pedido = buscarPedidoAberto(request, mesa1)  
    
    #produto que eu vou modificar estoque     
    vProduto = Produto.objects.get(pk=cod_produto) 
    #produtos que estão em pedido
    produto=Pedido_Produto.objects.filter(cod_pedido=pedido.cod, cod_produto=vProduto.cod) 
    for i in produto:
        if i.cod_produto.cod==vProduto.cod: #busco o produto especifico
            if i.quantidade==quantidadeDeletar:
                i.delete() #se a quantidade for igual, deleta do banco
            else:
                i.quantidade-=quantidadeDeletar
                i.save() # se não, só modifica o valor
    #modifico o valor do pedido e o estoque do produto
    pedido.valor-=quantidadeDeletar*vProduto.valorUnitario
    pedido.save()
    vProduto.estoque+=quantidadeDeletar
    vProduto.save()
    
    return redirect("/pedidos/"+str(mesa1)+"/carrinho/") #retorno pro cardapio

#Método que direciona para a tela de confiração
def confirmarPedido(request, mesa1):
    pedido=buscarPedidoAberto(request, mesa1)
    contexto = {'mesa': mesa1, 'vPedido': pedido}
    return render(request, "pedidos/carrinhoConfirmar.html", contexto) 

#Método que confirma o pedido
def confirmarPedidoFinal(request, mesa1):
    pedido=buscarPedidoAberto(request, mesa1)
    #busco a observação no banco e altero o pedido
    observ = str(request.POST.get('observacao'))
    pedido.observacao=observ
    pedido.status=1 #mudo o status do pedido para em preparo
    pedido.save()
    #altero a comanda
    comanda=buscarComanda(request, mesa1)
    comanda.valorTotal+=pedido.valor
    comanda.save() 
    
    return redirect("/"+str(mesa1)+"/cardapio/") 

#----------------------------------------------> Comandas <----------------------------------------------
#Método que lista os pedidos da Comanda
def list_comanda(request, mesa1):
    comanda=buscarComanda(request, mesa1)
    dsPedidos = Pedido.objects.filter(comanda=comanda)
    if dsPedidos.count()==0:
        mesaContext={'mesa':mesa1}
        return render(request, "pedidos/carrinhoVazio.html", mesaContext)
    else:
        contexto={'comanda': comanda, 'mesa': mesa1, 'dsPedidos': dsPedidos}
        return render(request, "pedidos/comanda.html", contexto)

#Método que irá detalhar o pedido especifico    
def detalharPedido():
    print("Cry")

#método que busca comanda a partir da mesa
def buscarComanda(request, mesa1):
    mesaContext={'mesa': mesa1}
    dsComanda = Comanda.objects.filter(status=0, mesa=mesa1) 
    if dsComanda.count()== 0: #verifico se não há comanda
        return render(request, "pedidos/carrinhoVazio.html", mesaContext) #se não tiver
    else:
        for i in dsComanda: #se tiver busco
            comanda = i
        return comanda
#método que busca pedido a partir da mesa
def buscarPedidoAberto(request, mesa1):
    dsPedido = Pedido.objects.filter(status=0, comanda=buscarComanda(request, mesa1))
    if dsPedido.count()==0: #verifico se há pedido
        mesaContext={'mesa':mesa1}
        return render(request, "pedidos/carrinhoVazio.html", mesaContext)
    else: #se houver, busca ele
        for a in dsPedido:
            pedido = a
        return pedido