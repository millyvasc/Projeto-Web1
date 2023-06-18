from produtos.models import Produto
from comandas.models import Comanda
from django.db import models

class Pedido(models.Model):
    cod = models.BigAutoField(primary_key=True) #BigAutoField, pra ser auto incrementável
    produtos = models.ManyToManyField(Produto, related_name="Produtos")#Muitos produtos, podem estar em muitos pedidos
    comanda = models.ForeignKey(Comanda, on_delete=models.CASCADE)
    valor = models.DecimalField(default = 0.00, max_digits=10, decimal_places=2)
    observacao = models.CharField(max_length=200)
    
    def adicicionar(self, cod_produto, quantidade):
        produto = Produto.objects.get(pk=cod_produto)
        for a in quantidade:
            self.produtos+=produto
            self.calor+=produto.valor_unitario
        self.save()
        
    def concluir(self, cod_comanda):
        self.comanda=cod_comanda
        comanda = Comanda.objects.get(pk=cod_comanda)
        comanda.valorTotal+=self.valor
        

    def __str__(self):
        return "Pedido "+str(self.cod)