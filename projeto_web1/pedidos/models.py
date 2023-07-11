from produtos.models import Produto
from comandas.models import Comanda
from django.db import models

# --
from django.utils import timezone

class Pedido(models.Model):
    cod = models.BigAutoField(primary_key=True)
    comanda = models.ForeignKey(Comanda, on_delete=models.CASCADE, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    observacao = models.CharField(max_length=200, blank=True)
    status = models.IntegerField(default=0) # 0 = EM ABERTO  | 1 = EM PREPARO  | 2 = ENTREGUE
    def __str__(self):
        return "Pedido "+str(self.cod)

class Pedido_Produto(models.Model):
    cod = models.BigAutoField(primary_key=True)
    cod_pedido=models.ForeignKey(Pedido, on_delete=models.CASCADE, blank=True)
    cod_produto=models.ForeignKey(Produto, on_delete=models.CASCADE, blank=True)
    quantidade = models.IntegerField()

    def __str__(self):
        return str(self.cod)