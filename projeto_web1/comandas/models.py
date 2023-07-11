from django.db import models

class Comanda(models.Model):

    cod = models.BigAutoField(primary_key=True)
    valorTotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mesa = models.IntegerField()
    status = models.IntegerField(default=0)  # 0 = EM ABERTO | 1 = Finalizado
    opcaoPagamento = models.CharField(max_length=20, blank=True)
    troco = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    data_e_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Comanda "+str(self.cod)