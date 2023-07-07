from comandas.models import Comanda
from produtos.models import Produto
from pedidos.models import Pedido, Pedido_Produto
from django.shortcuts import redirect, render

# ---- Utilizados para os métodos de geração e impressão de documentos, além de verificar as impressoras disponíveis e definir uma padrão  -------------------
from datetime import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import win32print
import win32api
# from win32.win32print import win32print

# ------------------------------------------------------------

def adicionar(request, mesa1, cod_produto):
    # crio ou busco a comanda
    dsComanda = Comanda.objects.filter(status=0, mesa=mesa1)
    if dsComanda.count() == 0:
        #vejo se tem alguma comanda esperando pagamento
        dsComanda1 = Comanda.objects.filter(status=1, mesa=mesa1)
        if dsComanda1.count() == 0: #se não tiver, crio uma nova
            comanda = Comanda()
            comanda.mesa = mesa1
            comanda.save()
        else:
            #se houver, mando pra ela
            return redirect("/comandas/"+str(mesa1)+"/")
    else:
        for i in dsComanda:
            if i.status == 0:
                comanda = Comanda.objects.get(pk=i.cod)

    # busco o pedido em aberto daquela comanda
    dsPedido = Pedido.objects.filter(status=0, comanda=comanda.cod)
    if dsPedido.count() == 0:  # se não houver pedido em andamento cria um
        pedido = Pedido()
        pedido.comanda = comanda
        pedido.save()
    else:  # se houver, busca ele
        for i in dsPedido:
            if i.status == 0:
                pedido = Pedido.objects.get(pk=i.cod)

    # pego a quantidade do form
    quantidade = int(request.POST.get('quantidade'))

    # busco o pedido
    produto = Produto.objects.get(pk=cod_produto)

    # salvo o produto no "pedido"
    produtosPedidos = Pedido_Produto.objects.filter(
        cod_pedido=pedido.cod, cod_produto=produto.cod)
    if produtosPedidos.count() == 0:  # guardo no banco se não houver daquele produto
        produtos = Pedido_Produto()
        produtos.cod_pedido = pedido
        produtos.cod_produto = produto
        produtos.quantidade = quantidade
        produtos.save()
    else:  # se ja tiver, busco ele e modifico a quantidade
        for i in produtosPedidos:
            i.quantidade += quantidade
            i.save()

    # altero os valores e estoque
    pedido.valor += (produto.valorUnitario*quantidade)
    pedido.save()
    produto.estoque = (produto.estoque-quantidade)
    produto.save()

    return redirect("/"+str(mesa1)+"/cardapio/")  # retorno pro cardapio

# Método para listar todos pedido do carrinho (Alterei ele - Camille)
def list_carrinho(request, mesa1):
    mesaContext = {'mesa': mesa1}
    dsComanda = Comanda.objects.filter(status=0, mesa=mesa1)
    if dsComanda.count() == 0:  # verifico se não há comanda
        # se não tiver
        return render(request, "pedidos/carrinhoVazio.html", mesaContext)
    else:
        for i in dsComanda:  # se tiver busco
            if i.status == 0:
                comanda = Comanda.objects.get(pk=i.cod)

        dsPedido = Pedido.objects.filter(status=0, comanda=comanda.cod)
        if dsPedido.count() == 0:  # verifico se há pedidp
            return render(request, "pedidos/carrinhoVazio.html", mesaContext)
        else:  # se houver, busca ele
            for i in dsPedido:
                if i.status == 0:
                    pedido = Pedido.objects.get(pk=i.cod)

            produtosPedidos = Pedido_Produto.objects.filter(
                cod_pedido=pedido.cod)
            # Verifico se há produtos no pedido
            if produtosPedidos.count() == 0:
                return render(request, "pedidos/carrinhoVazio.html", mesaContext)
            else:
                # filtragem :
                dsProdutosAux = Produto.objects.all()
                dsProdutos = []

                soma = 0  #F guardo o valor total do pedido
                for i in produtosPedidos:
                    for a in dsProdutosAux:  # guardo os produtos
                        if i.cod_produto.cod == a.cod:
                            i.cod_produto.estoque = i.quantidade
                            i.cod_produto.valorUnitario = i.quantidade*i.cod_produto.valorUnitario
                            dsProdutos.append(i.cod_produto)
                            soma = soma+(a.valorUnitario*i.quantidade)

                contexto = {'mesa': mesa1,
                            'dsProdutos': dsProdutos, 'soma': soma, 'pedido': pedido}
                return render(request, "pedidos/carrinho.html", contexto)

# Método para remover algo do carrinho

def remover_carrinho(request, mesa1, cod_produto):
    pedido = buscarPedidoAberto(request, mesa1)
    vProduto = Produto.objects.get(pk=cod_produto)
    produto = Pedido_Produto.objects.filter(
        cod_pedido=pedido.cod, cod_produto=vProduto.cod)
    # altero os valores de estoque dos produtos, para a quantidade do produto no pedido
    for i in produto:
        if i.cod_produto.cod == vProduto.cod:
            vProduto.estoque = i.quantidade

    contexto = {'mesa': mesa1, 'vProduto': vProduto}
    return render(request, "pedidos/carrinhoRemover.html", contexto)

# Método que confirma a remoção

def remover_carrinho_confirmar(request, mesa1, cod_produto):
    # Busco a quantidade a se remover
    quantidadeDeletar = int(request.POST.get('quantidade'))
    pedido = buscarPedidoAberto(request, mesa1)

    # produto que eu vou modificar estoque
    vProduto = Produto.objects.get(pk=cod_produto)
    # produtos que estão em pedido
    produto = Pedido_Produto.objects.filter(
        cod_pedido=pedido.cod, cod_produto=vProduto.cod)
    for i in produto:
        if i.cod_produto.cod == vProduto.cod:  # busco o produto especifico
            if i.quantidade == quantidadeDeletar:
                i.delete()  # se a quantidade for igual, deleta do banco
                
            else:
                i.quantidade -= quantidadeDeletar
                i.save()  # se não, só modifica o valor
    # modifico o valor do pedido e o estoque do produto
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
        return redirect("/"+str(mesa1)+"/cardapio/")
    else:
        return redirect("/pedidos/"+str(mesa1)+"/carrinho/")
    
    comanda = pedido.comanda
    pedido.delete()
    pedidos = Pedido.objects.filter(comanda=comanda.cod)
    if pedidos.count() == 0:
        comanda.delete()
        
    #deleção de pedidos e comanda caso estejam vazios
    

def gerar_pdf_impressao_pedido(mesa1, pedido, produtos_pedido):
    import uuid
    #sufixo exclusivo com base no timestamp atual
    # timestamp = str(int(uuid.uuid4()))
    timestamp = datetime.now().strftime("%d-%m-%Y_%Hh%Mmin%Sseg")
    # timestamp = timestamp[:8]
    # Criação do objeto canvas para gerar o PDF
    nome_arquivo = f"impressao_pedido_#{pedido.cod}_{timestamp}.pdf"
    c = canvas.Canvas(os.path.join("pdf_pedidos", nome_arquivo), pagesize=letter)
    # c = canvas.Canvas("impressao_pedido.pdf", pagesize=letter)

    # Adicione os elementos do pedido ao PDF
    # data_hora_formatada = pedido.data_hora.strftime('%d/%m/%Y %H:%M:%S')
    if pedido is not None:
        c.setFont("Helvetica", 12)
        c.drawString(100, 760, f"PEDIDO GERADO")
        c.drawString(100, 740, f"Mesa Nº: {mesa1}")
        c.drawString(100, 720, f"Comanda Nº: {pedido.comanda_id}")
        c.drawString(100, 700, f"Pedido Nº: {pedido.cod}")
        # c.drawString(100, 680, f"Data e Hora: {data_hora_formatada}")
        c.drawString(100, 660, "Produtos:")
    else:
        print("Pedido é None")
        
        
    y = 640
    for produto_pedido in produtos_pedido:
        cod_produto = produto_pedido.cod_produto_id
        produto = produto_pedido.cod_produto.nome
        quantidade = produto_pedido.quantidade
        c.drawString(120, y, f"-> Código: {cod_produto} - Produto: {produto} - Quantidade: {quantidade}")
        y -= 20

    # Salve o arquivo PDF
    c.showPage()
    c.save()
    
    return os.path.join("pdf_pedidos", nome_arquivo)

def gerar_pdf_cancelamento(mesa1, pedido, produtos_pedido):
    #sufixo exclusivo com base no timestamp atual
    # timestamp = str(int(uuid.uuid4()))
    timestamp = datetime.now().strftime("%d-%m-%Y_%Hh%Mmin%Sseg")
    # timestamp = timestamp[:8]
    # Criação do objeto canvas para gerar o PDF
    nome_arquivo = f"impressao_cancelamento_pedido_#{pedido.cod}_{timestamp}.pdf"
    c = canvas.Canvas(os.path.join("pdf_cancelamentos", nome_arquivo), pagesize=letter)
    # c = canvas.Canvas("impressao_pedido.pdf", pagesize=letter)

    # Adicione os elementos do pedido ao PDF
    # data_hora_formatada = pedido.data_hora.strftime('%d/%m/%Y %H:%M:%S')
    if pedido is not None:
        c.setFont("Helvetica", 12)
        c.drawString(100, 760, f"ALERTA! CANCELAMENTO DE PEDIDO Nº {pedido.cod}")
        c.drawString(100, 740, f"Mesa Nº: {mesa1}")
        c.drawString(100, 720, f"Comanda Nº: {pedido.comanda_id}")
        c.drawString(100, 700, f"Pedido Nº: {pedido.cod}")
        # c.drawString(100, 680, f"Data e Hora: {data_hora_formatada}")
        c.drawString(100, 660, "Produtos:")
    else:
        print("Pedido é None")
        
        
    y = 640
    for produto_pedido in produtos_pedido:
        cod_produto = produto_pedido.cod_produto_id
        produto = produto_pedido.cod_produto.nome
        quantidade = produto_pedido.quantidade
        c.drawString(120, y, f"(X) Código: {cod_produto} - Produto: {produto} - Quantidade: {quantidade}")
        y -= 20

    # Salve o arquivo PDF
    c.showPage()
    c.save()
    
    return os.path.join("pdf_cancelamentos", nome_arquivo)
    

# def enviar_pedido_impressora(mesa1, pedido, produtos_pedido):
def enviar_impressora(arquivo_pdf):

    # Implementando a lógica para enviar o pedido para a impressora
    
    # arquivo_pdf = gerar_pdf_impressao_pedido(mesa1, pedido, produtos_pedido)
    
    # arquivo_pdf_cancelamento = gerar_pdf_cancelamento(mesa1, pedido, produtos_pedido)
    # definir_impressora_padrao()
    
    
    # A linha abaixo envia o comando shell para a impressora e imprime o arquivo
    if arquivo_pdf is not None:
        print("Enviando para impressora")
        win32api.ShellExecute(0, "print", arquivo_pdf, None, ".", 0)
    
    
    # listar_impressoras()
    # definir_impressora_padrao()s
    impressora_padrao = win32print.GetDefaultPrinter() #pegando impressora padrão do sistema
    print("Impressora Padrão: " + impressora_padrao)
    

def listar_impressoras():
    impressoras = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)

    print("Impressoras Disponíveis:")
    for i, impressora in enumerate(impressoras):
        nome_impressora = impressora[2]
        print(f"{i+1}. {nome_impressora}")


    opcao = int(input("Ecolha uma das opções e digite o número da impressora desejada: "))
    if opcao >= 1 and opcao <= len(impressoras):
        return impressoras[opcao-1][2]
    else:
        print("Opção inválida.")
        return None
    
def definir_impressora_padrao():
    impressora_atual = win32print.GetDefaultPrinter()
    # impressora_atual = None # Isso é para que nenhuma impressora seja atribuída ao sistema
    
# if impressora_atual is None:
    print(f"Impressora padrão atual: {impressora_atual}")
    # print("Nenhuma impressora padrão selecionada.")
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
def confirmarPedidoFinal(request, mesa1, cod_pedido):
    
    #pedido = buscarPedidoAberto(request, mesa1)
    pedido = Pedido.objects.get(pk=cod_pedido)
    # busco a observação no banco e altero o pedido
    observ = str(request.POST.get('observacao'))
    pedido.observacao = observ
    pedido.status = 1  # mudo o status do pedido para em preparo
    pedido.save()
    
    # altero a comanda
    comanda = buscarComanda(request, mesa1)
    comanda.valorTotal += pedido.valor
    comanda.save()
    
    produtosPedido = Pedido_Produto.objects.filter(cod_pedido=pedido.cod)
    # Verifico se há produtos no pedido
    if produtosPedido.count() == 0:
        return render(request, "pedidos/carrinhoVazio.html")
    else:
        # filtragem :
        dsProdutosPedido = Produto.objects.all()
    
    #pdf_pedido = gerar_pdf_impressao_pedido(mesa1, pedido, produtosPedido)
    
    #enviar_impressora(pdf_pedido) #método para enviar o pedido para a impressora
    #definir_impressora_padrao() #Método para definir uma impressora padrão para o sistema

    return redirect("/"+str(mesa1)+"/cardapio/")

def modificarPedido(request, mesa1, cod_pedido):
    pedidoModificando = Pedido.objects.get(pk=cod_pedido)
    comanda = pedidoModificando.comanda
    pedidosCarrinho = Pedido.objects.filter(comanda=comanda.cod, status=0)
    
    if pedidoModificando.status != 0:
        
        if pedidosCarrinho.count()==0: #não tem carrinho
            pedidoModificando.status=0 
            comanda.valorTotal -= pedidoModificando.valor
            comanda.save()
            #
            #Aqui a geração de pdf para cancelamento do pedido modificando
            #
            pedidoModificando.save()
        
    return redirect("/pedidos/"+str(mesa1)+"/carrinho/")

def deletarPedido(request, mesa1, cod_pedido):
    pedido = Pedido.objects.get(pk=cod_pedido)
    produtosAux = Produto.objects.all()
    produtos = []
    produtosPedidos = Pedido_Produto.objects.filter(cod_pedido=pedido.cod)

    for i in produtosPedidos:
        for a in produtosAux:
            if i.cod_produto.cod == a.cod:  # salvo os produtoos, mas antes
                # mudo o valorUnitario para a soma de todos os produtos iguais
                i.cod_produto.valorUnitario = (
                    a.valorUnitario*i.quantidade)
                # 'salvo' a quantidade de produtos do pedido no estoque do produto
                i.cod_produto.estoque = i.quantidade
                i.cod_produto.cod = pedido.cod  # 'salvo' o id do pedido no id do produto                    # isso tudo é apenas para a visualização no html, pois não modifico o produto no BD
                produtos.append(i.cod_produto)
                
    
    contexto = {'mesa': mesa1, 'pedido': pedido, 'produtos': produtos}
    
    return render(request, "pedidos/deletar.html", contexto)

def deletarPedidoFinal(request, mesa1, cod_pedido):
    pedido = Pedido.objects.get(pk=cod_pedido)
    #reaver valores e estoque
    if pedido.status!=0:
        pedido.comanda.valorTotal=pedido.comanda.valorTotal-pedido.valor
        pedido.comanda.save()
    produtosAux = Produto.objects.all()
    produtosPedidos = Pedido_Produto.objects.filter(cod_pedido=pedido.cod)

    for produtoPedido in produtosPedidos:
        for produto in produtosAux:
            if produtoPedido.cod_produto.cod == produto.cod:  # salvo os produtoos, mas antes
                produto.estoque=produto.estoque+produtoPedido.quantidade
                produto.save()
                
    #
    # Aqui a emissão do pdf
    
    #pdf_cancelamento = gerar_pdf_cancelamento(mesa1, pedido, produtosPedidos)
    #enviar_impressora(pdf_cancelamento)
    #
    
    #deleção de pedidos e comanda caso estejam vazios
    
    comanda = pedido.comanda
    pedido.delete()
    pedidos = Pedido.objects.filter(comanda=comanda.cod)
    if pedidos.count() == 0:
        comanda.delete()
    
    return redirect("/"+str(mesa1)+"/cardapio/")

# ----------------------------------------------> Comandas <----------------------------------------------

# Método de detalhamento da comanda


# método que busca comanda a partir da mesa


def buscarComanda(request, mesa1):
    mesaContext = {'mesa': mesa1}
    dsComanda = Comanda.objects.filter(status=0, mesa=mesa1)
    if dsComanda.count() == 0:  # verifico se não há comanda
        # se não tiver
        return render(request, "pedidos/carrinhoVazio.html", mesaContext)
    else:
        for i in dsComanda:  # se tiver busco
            comanda = i
        return comanda
# método que busca pedido a partir da mesa


def buscarPedidoAberto(request, mesa1):
    dsPedido = Pedido.objects.filter(
        status=0, comanda=buscarComanda(request, mesa1))
    if dsPedido.count() == 0:  # verifico se há pedido
        mesaContext = {'mesa': mesa1}
        return render(request, "pedidos/carrinhoVazio.html", mesaContext)
    else:  # se houver, busca ele
        for a in dsPedido:
            pedido = a
        return pedido