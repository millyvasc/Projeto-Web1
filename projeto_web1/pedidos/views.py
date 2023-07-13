from comandas.models import Comanda
from produtos.models import Produto
from pedidos.models import Pedido, Pedido_Produto
from django.shortcuts import redirect, render
from datetime import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import win32print
import win32api


def adicionar(request, cod_produto):
    mesa1 = request.session.get('mesa')
    # crio ou busco a comanda

    dsComanda = Comanda.objects.filter(status=0, mesa=mesa1)
    if dsComanda.count() == 0:
        dsComanda1 = Comanda.objects.filter(status=1, mesa=mesa1)
        if dsComanda1.count() == 0:
            comanda = Comanda()
            comanda.mesa = mesa1
            nova_data_e_hora = datetime.now()
            comanda.data_e_hora = nova_data_e_hora
            comanda.save()
        else:

            #se houver, mando pra ela
            return redirect("/comandas/")

    else:
        for i in dsComanda:
            if i.status == 0:
                comanda = Comanda.objects.get(pk=i.cod)
    dsPedido = Pedido.objects.filter(status=0, comanda=comanda.cod)
    if dsPedido.count() == 0:
        pedido = Pedido()
        pedido.comanda = comanda
        pedido.save()
    else:
        for i in dsPedido:
            if i.status == 0:
                pedido = Pedido.objects.get(pk=i.cod)
    quantidade = int(request.POST.get('quantidade'))
    produto = Produto.objects.get(pk=cod_produto)
    if quantidade > produto.estoque:
        quantidade = produto.estoque
    produtosPedidos = Pedido_Produto.objects.filter(
        cod_pedido=pedido.cod, cod_produto=produto.cod)
    if produtosPedidos.count() == 0:
        produtos = Pedido_Produto()
        produtos.cod_pedido = pedido
        produtos.cod_produto = produto
        produtos.quantidade = quantidade
        produtos.save()
    else:
        for i in produtosPedidos:
            i.quantidade += quantidade
            i.save()
    pedido.valor += (produto.valorUnitario*quantidade)
    pedido.save()
    produto.estoque = (produto.estoque-quantidade)
    produto.save()

    return redirect("/cardapio/cardapio/")  # retorno pro cardapio


# Método para listar todos pedido do carrinho (Alterei ele - Camille)
def list_carrinho(request):
    mesa1 = request.session.get('mesa')

    mesaContext = {'mesa': mesa1}
    dsComanda = Comanda.objects.filter(status=0, mesa=mesa1)
    if dsComanda.count() == 0:
        return render(request, "pedidos/carrinhoVazio.html", mesaContext)
    else:
        for i in dsComanda:
            if i.status == 0:
                comanda = Comanda.objects.get(pk=i.cod)
        dsPedido = Pedido.objects.filter(status=0, comanda=comanda.cod)
        if dsPedido.count() == 0:
            return render(request, "pedidos/carrinhoVazio.html", mesaContext)
        else:
            for i in dsPedido:
                if i.status == 0:
                    pedido = Pedido.objects.get(pk=i.cod)
            produtosPedidos = Pedido_Produto.objects.filter(
                cod_pedido=pedido.cod)
            if produtosPedidos.count() == 0:
                return render(request, "pedidos/carrinhoVazio.html", mesaContext)
            else:
                dsProdutosAux = Produto.objects.all()
                dsProdutos = []
                soma = 0
                for i in produtosPedidos:
                    for a in dsProdutosAux:
                        if i.cod_produto.cod == a.cod:
                            i.cod_produto.estoque = i.quantidade
                            i.cod_produto.valorUnitario = i.quantidade*i.cod_produto.valorUnitario
                            dsProdutos.append(i.cod_produto)
                            soma = soma+(a.valorUnitario*i.quantidade)
                contexto = {'mesa': mesa1,
                            'dsProdutos': dsProdutos, 'soma': soma, 'pedido': pedido}
                return render(request, "pedidos/carrinho.html", contexto)


def remover_carrinho(request, mesa1, cod_produto):
    dsPedido = Pedido.objects.filter(
        status=0, comanda=buscarComanda(request, mesa1))
    if dsPedido.count() == 0:
        mesaContext = {'mesa': mesa1}
        return render(request, "pedidos/carrinhoVazio.html", mesaContext)
    else:
        for a in dsPedido:
            pedido = a

    vProduto = Produto.objects.get(pk=cod_produto)
    produto = Pedido_Produto.objects.filter(
        cod_pedido=pedido.cod, cod_produto=vProduto.cod)
    for i in produto:
        if i.cod_produto.cod == vProduto.cod:
            vProduto.estoque = i.quantidade
    contexto = {'mesa': mesa1, 'vProduto': vProduto}
    return render(request, "pedidos/carrinhoRemover.html", contexto)



def remover_carrinho_confirmar(request, cod_produto):

    mesa1 = request.session.get('mesa')
    # Busco a quantidade a se remover

    quantidadeDeletar = int(request.POST.get('quantidade'))
    dsPedido = Pedido.objects.filter(
        status=0, comanda=buscarComanda(request, mesa1))
    if dsPedido.count() == 0:
        mesaContext = {'mesa': mesa1}
        return render(request, "pedidos/carrinhoVazio.html", mesaContext)
    else:
        for a in dsPedido:
            pedido = a
    vProduto = Produto.objects.get(pk=cod_produto)
    produto = Pedido_Produto.objects.filter(
        cod_pedido=pedido.cod, cod_produto=vProduto.cod)
    for i in produto:
        if i.cod_produto.cod == vProduto.cod:
            if i.quantidade == quantidadeDeletar:
                i.delete()
            else:
                i.quantidade -= quantidadeDeletar
                i.save()
    pedido.valor -= quantidadeDeletar*vProduto.valorUnitario
    pedido.save()
    vProduto.estoque = (vProduto.estoque+quantidadeDeletar)
    vProduto.save()
    comanda = pedido.comanda
    produtos = Pedido_Produto.objects.filter(cod_pedido=pedido.cod)
    if produtos.count() == 0:
        pedido.delete()
        pedidos = Pedido.objects.filter(comanda=comanda.cod)
        if pedidos.count() == 0:
            comanda.delete()
        return redirect("/cardapio/cardapio/")
    else:

        return redirect("/pedidos/carrinho/")
        
    #deleção de pedidos e comanda caso estejam vazios

def gerar_pdf_impressao_pedido(mesa1, pedido, produtos_pedido):
    import uuid
    timestamp = datetime.now().strftime("%d-%m-%Y_%Hh%Mmin%Sseg")
    nome_arquivo = f"impressao_pedido_#{pedido.cod}_{timestamp}.pdf"
    c = canvas.Canvas(os.path.join(
        "pdf_pedidos", nome_arquivo), pagesize=letter)
    if pedido is not None:
        c.setFont("Helvetica", 12)
        c.drawString(100, 760, f"PEDIDO GERADO")
        c.drawString(100, 740, f"Mesa Nº: {mesa1}")
        c.drawString(100, 720, f"Comanda Nº: {pedido.comanda_id}")
        c.drawString(100, 700, f"Pedido Nº: {pedido.cod}")
        c.drawString(100, 660, "Produtos:")
    else:
        print("Pedido é None")
    y = 640
    for produto_pedido in produtos_pedido:
        cod_produto = produto_pedido.cod_produto_id
        produto = produto_pedido.cod_produto.nome
        quantidade = produto_pedido.quantidade
        c.drawString(
            120, y, f"-> Código: {cod_produto} - Produto: {produto} - Quantidade: {quantidade}")
        y -= 20
    c.showPage()
    c.save()

    
     # Verifica se a pasta "pdf_pedidos" existe
    if not os.path.exists("pdf_pedidos"):
        os.makedirs("pdf_pedidos")
    
    return os.path.join("pdf_pedidos", nome_arquivo)


def gerar_pdf_cancelamento(mesa1, pedido, produtos_pedido):
    timestamp = datetime.now().strftime("%d-%m-%Y_%Hh%Mmin%Sseg")
    nome_arquivo = f"impressao_cancelamento_pedido_#{pedido.cod}_{timestamp}.pdf"
    c = canvas.Canvas(os.path.join("pdf_cancelamentos",
                      nome_arquivo), pagesize=letter)
    if pedido is not None:
        c.setFont("Helvetica", 12)
        c.drawString(
            100, 760, f"ALERTA! CANCELAMENTO DE PEDIDO Nº {pedido.cod}")
        c.drawString(100, 740, f"Mesa Nº: {mesa1}")
        c.drawString(100, 720, f"Comanda Nº: {pedido.comanda_id}")
        c.drawString(100, 700, f"Pedido Nº: {pedido.cod}")
        c.drawString(100, 660, "Produtos:")
    else:
        print("Pedido é None")
    y = 640
    for produto_pedido in produtos_pedido:
        cod_produto = produto_pedido.cod_produto_id
        produto = produto_pedido.cod_produto.nome
        quantidade = produto_pedido.quantidade
        c.drawString(
            120, y, f"(X) Código: {cod_produto} - Produto: {produto} - Quantidade: {quantidade}")
        y -= 20
    c.showPage()
    c.save()

    
     # Verifica se a pasta "pdf_pedidos" existe
    if not os.path.exists("pdf_cancelamentos"):
        os.makedirs("pdf_cancelamentos")
    

    return os.path.join("pdf_cancelamentos", nome_arquivo)


# def enviar_pedido_impressora(mesa1, pedido, produtos_pedido):
# def enviar_impressora(arquivo_pdf):
fila_pedidos = []
fila_cancelamentos = []
def enviar_impressora():
    # Implementando a lógica para enviar o pedido para a impressora
    
    # arquivo_pdf = gerar_pdf_impressao_pedido(mesa1, pedido, produtos_pedido)
    
    # arquivo_pdf_cancelamento = gerar_pdf_cancelamento(mesa1, pedido, produtos_pedido)
    # definir_impressora_padrao()
    
    
    # A linha abaixo envia o comando shell para a impressora e imprime o arquivo
    # if arquivo_pdf is not None:
    #     print("Enviando para impressora")
    #     win32api.ShellExecute(0, "print", arquivo_pdf, None, ".", 0)
    
    # TESTE NOVO ---------
    # Verifica se há um pedido de cancelamento na fila de cancelamentos
    # Exibir todos os itens da fila de pedidos
    print("Itens na fila de Pedidos:")
    for arquivo_pedido in fila_pedidos:
        print("-", arquivo_pedido)

    print("Itens na fila de Cancelamentos:")
    for arquivo_cancelamento in fila_cancelamentos:
        print("-", arquivo_cancelamento)
        
    definir_impressora_padrao()
   
    if fila_cancelamentos:
        arquivo_cancelamento = fila_cancelamentos[0]
        print("Enviando para impressora (CANCELAMETNO): ", arquivo_cancelamento)
        win32api.ShellExecute(0, "print", arquivo_cancelamento, None, ".", 0) 
        
    # Caso contrário, envia o próximo pedido da fila de pedidos pendentes
    if fila_pedidos:
        arquivo_pedido = fila_pedidos[0]
        print("Enviando para impressora (PEDIDO):", arquivo_pedido)
        win32api.ShellExecute(0, "print", arquivo_pedido, None, ".", 0)
    else:
        print("Não há pedidos para imprimir.")
    
    # listar_impressoras()
    
     # Exibir novamente os itens nas filas após o envio
    print("Itens restantes na fila de Pedidos:")
    for arquivo_pedido in fila_pedidos:
        print("-", arquivo_pedido)

    print("Itens restantes na fila de Cancelamentos:")
    for arquivo_cancelamento in fila_cancelamentos:
        print("-", arquivo_cancelamento)
     
    impressora_padrao = win32print.GetDefaultPrinter() #pegando impressora padrão do sistema

    print("Impressora Padrão: " + impressora_padrao)


def listar_impressoras():
    impressoras = win32print.EnumPrinters(
        win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
    print("Impressoras Disponíveis:")
    for i, impressora in enumerate(impressoras):
        nome_impressora = impressora[2]
        print(f"{i+1}. {nome_impressora}")
    opcao = int(
        input("Ecolha uma das opções e digite o número da impressora desejada: "))
    if opcao >= 1 and opcao <= len(impressoras):
        return impressoras[opcao-1][2]
    else:
        print("Opção inválida.")
        return None


def definir_impressora_padrao():
    impressora_atual = win32print.GetDefaultPrinter()
    print(f"Impressora padrão atual: {impressora_atual}")
    opcao = input("Deseja definir outra impressora como padrão? (S/N): ")
    if opcao.lower() == "s":
        nova_impressora = listar_impressoras()
        if nova_impressora is not None:
            win32print.SetDefaultPrinter(nova_impressora)
            print(f"Impressora '{nova_impressora}' definida como padrão.")
    else:
        print("Nenhuma alteração realizada.")
    return


def obter_impressora_padrao():
    impressora_padrao = win32print.GetDefaultPrinter()
    print("Impressora padrão:", impressora_padrao)
    return impressora_padrao


   
# Método que confirma o pedido
def confirmarPedidoFinal(request, cod_pedido):
    mesa1 = request.session.get('mesa')
    
    #pedido = buscarPedidoAberto(request, mesa1)

    pedido = Pedido.objects.get(pk=cod_pedido)
    observ = str(request.POST.get('observacao'))
    pedido.observacao = observ
    pedido.status = 1
    pedido.save()
    comanda = pedido.comanda
    comanda.valorTotal += pedido.valor
    comanda.save()
    produtosPedido = Pedido_Produto.objects.filter(cod_pedido=pedido.cod)
    if produtosPedido.count() == 0:
        return render(request, "pedidos/carrinhoVazio.html")
    else:
        dsProdutosPedido = Produto.objects.all()

    
    # pdf_pedido = gerar_pdf_impressao_pedido(mesa1, pedido, produtosPedido)
    
    # if pdf_pedido is not None:
        # fila_pedidos.append(pdf_pedido)
    
    # enviar_impressora()
    #enviar_impressora(pdf_pedido) #método para enviar o pedido para a impressora
    #definir_impressora_padrao() #Método para definir uma impressora padrão para o sistema

    return redirect("/cardapio/cardapio")

def modificarPedido(request, cod_pedido):
    mesa1 = request.session.get('mesa')

    pedidoModificando = Pedido.objects.get(pk=cod_pedido)
    comanda = pedidoModificando.comanda
    pedidosCarrinho = Pedido.objects.filter(comanda=comanda.cod, status=0)
    if pedidoModificando.status != 0:
        if pedidosCarrinho.count() == 0:
            pedidoModificando.status = 0
            comanda.valorTotal -= pedidoModificando.valor
            comanda.save()
            pedidoModificando.save()
     
    return redirect("/pedidos/carrinho/")

def deletarPedido(request, cod_pedido):
    # request.session['cod_pedido'] = cod_pedido
    mesa1 = request.session.get('mesa')

    pedido = Pedido.objects.get(pk=cod_pedido)
    produtosAux = Produto.objects.all()
    produtos = []
    produtosPedidos = Pedido_Produto.objects.filter(cod_pedido=pedido.cod)
    for i in produtosPedidos:
        for a in produtosAux:
            if i.cod_produto.cod == a.cod:
                i.cod_produto.valorUnitario = (
                    a.valorUnitario*i.quantidade)
                i.cod_produto.estoque = i.quantidade
                i.cod_produto.cod = pedido.cod
                produtos.append(i.cod_produto)
    contexto = {'mesa': mesa1, 'pedido': pedido, 'produtos': produtos}
    return render(request, "pedidos/deletar.html", contexto)


def deletarPedidoFinal(request, cod_pedido):
  
    mesa1 = request.session.get('mesa')

    pedido = Pedido.objects.get(pk=cod_pedido)
    if pedido.status != 0:
        pedido.comanda.valorTotal = pedido.comanda.valorTotal-pedido.valor
        pedido.comanda.save()
    produtosAux = Produto.objects.all()
    produtosPedidos = Pedido_Produto.objects.filter(cod_pedido=pedido.cod)
    for produtoPedido in produtosPedidos:
        for produto in produtosAux:
            if produtoPedido.cod_produto.cod == produto.cod:
                produto.estoque = produto.estoque+produtoPedido.quantidade
                produto.save()

                
    #
    # Aqui a emissão do pdf
    
    # pdf_cancelamento = gerar_pdf_cancelamento(mesa1, pedido, produtosPedidos)
    
    # if pdf_cancelamento is not None:
        # fila_cancelamentos.append(pdf_cancelamento)
    
    # enviar_impressora()
    
    # enviar_impressora(pdf_cancelamento)
    #
    
    #deleção de pedidos e comanda caso estejam vazios
    
    comanda = pedido.comanda
    pedido.delete()
    pedidos = Pedido.objects.filter(comanda=comanda.cod)
    if pedidos.count() == 0:
        comanda.delete()

    return redirect("/cardapio/cardapio/")

# ----------------------------------------------> Comandas <----------------------------------------------


def buscarComanda(request, mesa1):
    mesaContext = {'mesa': mesa1}
    dsComanda = Comanda.objects.filter(status=0, mesa=mesa1)
    if dsComanda.count() == 0:
        return render(request, "pedidos/carrinhoVazio.html", mesaContext)
    else:
        for i in dsComanda:
            comanda = i
        return comanda


def buscarPedidoAberto(request, mesa1):
    dsPedido = Pedido.objects.filter(
        status=0, comanda=buscarComanda(request, mesa1))
    if dsPedido.count() == 0:
        mesaContext = {'mesa': mesa1}
        return render(request, "pedidos/carrinhoVazio.html", mesaContext)
    else:
        for a in dsPedido:
            pedido = a
        return pedido

    

# ---------------------- Referentes a garçom --------------------------
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

