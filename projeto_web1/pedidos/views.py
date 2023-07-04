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
import win32print
import win32api
# from win32.win32print import win32print

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




# import xml.etree.ElementTree as ET
#método para gerar xml do pedido
# def gerar_xml_pedido(mesa1, pedido, produtos_pedido):
#     # Cria o elemento raiz do XML
#     root = ET.Element("pedido")
    
#     # Adiciona elementos ao XML com base nos dados do pedido
#     mesa_element = ET.SubElement(root, "mesa")
#     mesa_element.text = str(mesa1)
    
#     codigo_element = ET.SubElement(root, "codigo")
#     codigo_element.text = str(pedido.cod)
    
#     data_hora_element = ET.SubElement(root, "data_hora")
#     data_hora_element.text = pedido.data_hora.strftime('%Y-%m-%d %H:%M:%S')
    
#     produtos_element = ET.SubElement(root, "produtos")
#     for produto_pedido in produtos_pedido:
#         produto_element = ET.SubElement(produtos_element, "produto")
#         nome_element = ET.SubElement(produto_element, "nome")
#         nome_element.text = produto_pedido.cod_produto.nome
#         quantidade_element = ET.SubElement(produto_element, "quantidade")
#         quantidade_element.text = str(produto_pedido.quantidade)
    
#     # Cria o objeto ElementTree com a estrutura XML
#     tree = ET.ElementTree(root)
    
#     # Salva o arquivo XML
#     arquivo_xml = os.path.join("pdf_pedidos", f"pedido_#{pedido.cod}.xml")
#     # arquivo_xml = f"pedido_#{pedido.cod}.xml"
#     tree.write(arquivo_xml, encoding="utf-8", xml_declaration=True)
    
#     return arquivo_xml

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
    data_hora_formatada = pedido.data_hora.strftime('%d/%m/%Y %H:%M:%S')
    if pedido is not None:
        c.setFont("Helvetica", 12)
        c.drawString(100, 740, f"Mesa Nº: {mesa1}")
        c.drawString(100, 720, f"Comanda Nº: {pedido.comanda_id}")
        c.drawString(100, 700, f"Pedido Nº: {pedido.cod}")
        c.drawString(100, 680, f"Data e Hora: {data_hora_formatada}")
        c.drawString(100, 660, "Produtos:")
    else:
        print("Pedido é None")
        
    # Adicione os detalhes de cada produto ao PDF
            # if produtos_pedido.cod_produto_id.tipo == "prato"  :
            #     pratos = produtos_pedido.objects.filter(tipo__icontains="prato").exclude(estoque=0)
                # pratos = produtos_pedido.objects.filter(
                 #     tipo__icontains="prato").exclude(estoque=0)
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
   

def obter_impressora_padrao():
    # Obtenha a impressora padrão
    impressora_padrao = win32print.GetDefaultPrinter()

    # Abra a impressora e obtenha um objeto PyHANDLE
    handle_impressora = win32print.OpenPrinter(impressora_padrao)

    # Obtenha informações sobre a impressora
    impressora_info = win32print.GetPrinter(handle_impressora, 2)

    # Extraia o nome da impressora
   # printer_info = win32print.GetPrinter("NomeDaImpressora", 2) # Osegundo argumento é sobre o nível de detalhe do retorno, 2 para obter informações completas
    nome_impressora = impressora_info["pPrinterName"]

    print("Impressora: " + nome_impressora)
    
    return nome_impressora #retorna o nome da impressora virtual 

def enviar_pedido_impressora(mesa1, pedido, produtos_pedido):
    # Implementando a lógica para enviar o pedido para a impressora
    
    # # Exemplo simplificado:
    # for produto_pedido in produtos_pedido:
    #     produto = produto_pedido.cod_produto.nome
    #     quantidade = produto_pedido.quantidade
    arquivo_pdf = gerar_pdf_impressao_pedido(mesa1, pedido, produtos_pedido)
    # gerar_xml_pedido(mesa1, pedido, produtos_pedido)
    
    # O a linha abaixo envia o comando shell para a impressora e imprime o pdf
    # win32api.ShellExecute(0, "print", arquivo_pdf, None, ".", 0)
    
    
    # Formate as informações e envie para a impressora
    # obter_impressora_padrao()
    
    
    
    # listar_impressoras()
    # definir_impressora_padrao()
    impressora_padrao = win32print.GetDefaultPrinter()
   
    
    
    # if impressora_padrao is None:
        # print("Não existe impressora padronizada")
        # definir_impressora_padrao()
    # else:
    print("Impressora Padrão: " + impressora_padrao)
    

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
        definir_impressora_padrao()
        contexto = { 'produtosPedido' : dsProdutosPedido}
            
    return redirect('/'+str(mesa1)+'/cardapio/') #retorno para cardapio




  # Variável global para armazenar o nome da impressora padrão
# impressora_padrao = None

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
    # impressora_atual = None
    # global impressora_padrao
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
# elif impressora_atual is not None:
#     print(f"Impressora padrão atual: {impressora_atual}")
        
        

    # opcao = input(f"Deseja definir a impressora '{impressora_padrao}' como padrão? (S/N): ")
    # if opcao.lower() == "s":
    #     win32print.SetDefaultPrinter(impressora_padrao)
    #     print(f"Impressora '{impressora_padrao}' definida como padrão.")
    # else:
    #     print("Nenhuma alteração realizada.")
        
        
def obter_impressora_padrao():
    impressora_padrao = win32print.GetDefaultPrinter()
    print("Impressora padrão:", impressora_padrao)
    return impressora_padrao        
