from comandas.models import Comanda
from urllib3 import HTTPResponse
from produtos.models import Produto
from pedidos.models import Pedido, Pedido_Produto
from django.shortcuts import redirect, render

# -------------------------------------------------------
from datetime import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ------------------------------------------------------------

def adicionar(request, mesa1, cod_produto):
    
    #se não houver comanda aberta na mesa, abre
    dsComanda = Comanda.objects.filter(status=0, mesa=mesa1) 
    #dsComandaTamanho = 
    if dsComanda.count()== 0:
        comanda = Comanda()
        comanda.mesa=mesa1
        comanda.save()
    #busco a comanda da mesa que esta em aberto (status=0)
    else:
        for i in dsComanda:
            if i.status==0:
                comanda = Comanda.objects.get(pk=i.cod)
    
    #busco o pedido em aberto daquela comanda
    dsPedido = Pedido.objects.filter(status=0, comanda=comanda.cod)
    
    dsPedidoTamanho = dsPedido.count() #pego o numero de itens no dsPedido
    
    if dsPedidoTamanho==0: #se não houver pedido em andamento cria um
        pedido = Pedido()
        pedido.comanda=comanda
        pedido.save()
    else: #se houver, busca ele
        for i in dsPedido:
            if i.status==0:
                pedido = Pedido.objects.get(pk=i.cod)
    
    
    #pego a quantidade do form
    quantidade = int(request.POST.get('quantidade'))
    
    print(str(quantidade))
    #busco o pedido
    produto = Produto.objects.get(pk=cod_produto)
    
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
    pedido.valor+=(produto.valorUnitario*int(quantidade))
    pedido.save()
    produto.estoque-=quantidade
    produto.save()
    
    
    return redirect("/"+str(mesa1)+"/cardapio/") #retorno pro cardapio

# Método para listar todos o carrinho
def list_carrinho(request, mesa1):
    
    dsComanda = Comanda.objects.filter(status=0, mesa=mesa1) 
    if dsComanda.count()== 0: #verifico se não há comanda
        return render(request, "pedidos/carrinhoVazio.html") #se não tiver
    else:
        for i in dsComanda: #se tiver busco
            if i.status==0:
                comanda = Comanda.objects.get(pk=i.cod)
        
        dsPedido = Pedido.objects.filter(status=0, comanda=comanda.cod)
        if dsPedido.count()==0: #verifico se há pedidp
            return render(request, "pedidos/carrinhoVazio.html")
        else: #se houver, busca ele
            for i in dsPedido:
                if i.status==0:
                    pedido = Pedido.objects.get(pk=i.cod)
        
            #pego todos os produtos do pedido
            produtosPedidos = Pedido_Produto.objects.filter(cod_pedido=pedido.cod)
            
            
            #filtragem :
            dsPratosAux = Produto.objects.filter(
                tipo__icontains="prato")#busco todos os pratos
            dsPratos=[]
            dsBebidasAux = Produto.objects.filter(
                tipo__icontains="bebida")
            dsBebidas=[]
            
            #busco os pratos
            for i in produtosPedidos:
                for a in dsPratosAux:
                    if i.cod_produto.cod==a.cod:
                        i.cod_produto.estoque=i.quantidade
                        dsPratos.append(i.cod_produto)
            #busco as bebidas
            for i in produtosPedidos:
                for a in dsBebidasAux:
                    if i.cod_produto.cod==a.cod:
                        i.cod_produto.estoque=i.quantidade
                        dsBebidas.append(i.cod_produto)
            
            
            contexto = {'mesa': mesa1, 'dsPratos': dsPratos, 'dsBebidas': dsBebidas, 'pedido' : pedido }
            
            return render(request, "pedidos/carrinho.html", contexto)
        
def remover_carrinho(request, mesa1, cod_produto):
    dsComanda = Comanda.objects.filter(status=0, mesa=mesa1) 
    if dsComanda.count()== 0: #verifico se não há comanda
        return render(request, "pedidos/carrinhoVazio.html") #se não tiver
    else:
        for i in dsComanda: #se tiver busco
            if i.status==0:
                comanda = Comanda.objects.get(pk=i.cod)
        
        dsPedido = Pedido.objects.filter(status=0, comanda=comanda.cod)
        if dsPedido.count()==0: #verifico se há pedidp
            return render(request, "pedidos/carrinhoVazio.html")
        else: #se houver, busca ele
            for i in dsPedido:
                if i.status==0:
                    pedido = Pedido.objects.get(pk=i.cod)
                    
    vProduto = Produto.objects.get(pk=cod_produto)
    produto=Pedido_Produto.objects.filter(cod_pedido=pedido.cod, cod_produto=vProduto.cod)
    for i in produto:
        if i.cod_produto.cod==vProduto.cod:
            vProduto.estoque=i.quantidade
    
    contexto = {'mesa': mesa1, 'vProduto': vProduto}
            
    return render(request, "pedidos/carrinhoRemover.html", contexto)

def remover_carrinho_confirmar(request, mesa1, cod_produto):
    quantidadeDeletar = int(request.POST.get('quantidade'))
    dsComanda = Comanda.objects.filter(status=0, mesa=mesa1) 
    if dsComanda.count()== 0: #verifico se não há comanda
        return render(request, "pedidos/carrinhoVazio.html") #se não tiver
    else:
        for i in dsComanda: #se tiver busco
            if i.status==0:
                comanda = Comanda.objects.get(pk=i.cod)
        
        dsPedido = Pedido.objects.filter(status=0, comanda=comanda.cod)
        if dsPedido.count()==0: #verifico se há pedidp
            return render(request, "pedidos/carrinhoVazio.html")
        else: #se houver, busca ele
            for i in dsPedido:
                if i.status==0:
                    pedido = Pedido.objects.get(pk=i.cod)
                    
    vProduto = Produto.objects.get(pk=cod_produto)
    produto=Pedido_Produto.objects.filter(cod_pedido=pedido.cod, cod_produto=vProduto.cod)
    for i in produto:
        if i.cod_produto.cod==vProduto.cod:
            vProduto.estoque=i.quantidade
            if vProduto.estoque==quantidadeDeletar:
                i.delete()
            else:
                i.quantidade-=quantidadeDeletar
                i.save()
    pedido.valor-=quantidadeDeletar*vProduto.valorUnitario
    pedido.save()
    vProduto.estoque+=quantidadeDeletar
    vProduto.save()
    
    return redirect("/pedidos/"+str(mesa1)+"/carrinho/") #retorno pro cardapio

def gerar_pdf_impressao_pedido(mesa1, pedido, produtos_pedido):
    import uuid
    #sufixo exclusivo com base no timestamp atual
    timestamp = str(int(uuid.uuid4()))
    timestamp = timestamp[:8]
    # Criação do objeto canvas para gerar o PDF
    c = canvas.Canvas(os.path.join("pdf_pedidos", f"impressao_pedido_#{pedido.cod}_{timestamp}.pdf"), pagesize=letter)
    # c = canvas.Canvas("impressao_pedido.pdf", pagesize=letter)

    # Adicione os elementos do pedido ao PDF
    data_hora_formatada = pedido.data_hora.strftime('%d/%m/%Y %H:%M:%S')
    if pedido is not None:
        c.setFont("Helvetica", 12)
        c.drawString(100, 720, f"Mesa: {mesa1}")
        c.drawString(100, 700, f"Código do Pedido: {pedido.cod}")
        c.drawString(100, 680, f"Data e Hora: {data_hora_formatada}")
        c.drawString(100, 660, "Produtos:")
    else:
        print("Pedido é None")
        
    # Adicione os detalhes de cada produto ao PDF
    y = 640
    for produto_pedido in produtos_pedido:
        produto = produto_pedido.cod_produto.nome
        quantidade = produto_pedido.quantidade
        c.drawString(120, y, f"- {produto}: {quantidade}")
        y -= 20

    # Salve o arquivo PDF
    c.showPage()
    c.save()

def enviar_pedido_impressora(mesa1, pedido, produtos_pedido):
    # Implemente a lógica para enviar o pedido para a impressora
    # Isso pode envolver a formatação adequada dos dados do pedido e o envio para a impressora usando a biblioteca ou serviço adequado.
    # Exemplo simplificado:
    for produto_pedido in produtos_pedido:
        produto = produto_pedido.cod_produto.nome
        quantidade = produto_pedido.quantidade
        
    gerar_pdf_impressao_pedido(mesa1, pedido, produtos_pedido)
    
        # Formate as informações e envie para a impressora


def fazer_pedido(request, mesa1, cod_pedido):
    dsComanda = Comanda.objects.filter(status=0, mesa=mesa1) 
    # dsPedidos =  Pedido.objects.filter(cod=cod_pedido)
    
    
    # dsComanda = Comanda.objects.filter(status=0, mesa=mesa1) 
    if dsComanda.count()== 0: #verifico se não há comanda
        return render(request, "pedidos/carrinhoVazio.html") #se não tiver
    else:
        for i in dsComanda: #se tiver busco
            if i.status==0:
                comanda = Comanda.objects.get(pk=i.cod)
        
        # dsPedido = Pedido.objects.filter(status=0, comanda=comanda.cod)
        pedido = Pedido.objects.get(pk=cod_pedido)
        pedido.data_hora = datetime.now()
        pedido.save()
        
        # if dsPedido.count()==0: #verifico se há pedidp
        #     return render(request, "pedidos/carrinhoVazio.html")
        # else: #se houver, busca ele
        #     for i in dsPedido:
        #         if i.status==0:
        #             pedido = Pedido.objects.get(pk=i.cod)
        
            #pego todos os produtos do pedido
            # produtosPedidos = Pedido_Produto.objects.filter(cod_pedido=pedido.cod)
        
            
        # pedido = Pedido.objects.filter(
        #     comanda=comanda,
        #     cod=cod_pedido,
        #     status=0,
        #     # data_hora=datetime.now()
        # ) 
        
        dsProdutosPedido = Pedido_Produto.objects.filter(cod_pedido=pedido.cod)
        
        enviar_pedido_impressora(mesa1, pedido, dsProdutosPedido) #método para enviar o pedido para a impressora
        
        contexto = { 'produtosPedido' : dsProdutosPedido}
            
    return redirect('/'+str(mesa1)+'/cardapio/') #retorno para cardapio

    # if dsPedidos.count()==0: #verifico se há pedido
    #     return render(request, "pedidos/carrinhoVazio.html")
    # else: #se houver, busca ele
    #     for i in dsPedidos:
    #         if i.status==0:
    #             pedido = Pedido.objects.get(pk=i.cod)

    
    
    # if dsComanda.count()== 0: #verifico se não há comanda
    #     return render(request, "pedidos/carrinhoVazio.html") #se não tiver
    # else:
    #     for i in dsComanda: #se tiver busco
    #         if i.status==0:
    #             comanda = Comanda.objects.get(pk=i.cod)
        
    #     dsPedido = Pedido.objects.filter(status=0, comanda=comanda.cod)
    #     if dsPedido.count()==0: #verifico se há pedidp
    #         return render(request, "pedidos/carrinhoVazio.html")
    #     else: #se houver, busca ele
    #         for i in dsPedido:
    #             if i.status==0:
    #                 pedido = Pedido.objects.get(pk=i.cod)
