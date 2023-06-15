from Produto.models import Produto
from Comanda.models import Comanda
from django.db import models

class Pedido(models.Model):
    cod = models.BigAutoField(primary_key=True) #BigAutoField, pra ser auto incrementável
    produtos = models.ManyToManyField(Produto, related_name="Produtos")#Muitos produtos, podem estar em muitos pedidos
    comanda = models.ForeignKey(Comanda, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    observacao = models.CharField(max_length=200)

    def __str__(self):
        return "Pedido "+str(self.cod)