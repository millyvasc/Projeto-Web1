from django.db import models


class Comanda(models.Model):
    # BigAutoField, pra ser auto incrementável
    cod = models.BigAutoField(primary_key=True)
    valorTotal = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    mesa = models.IntegerField()
    status = models.IntegerField(default=0)  # 0 = EM ABERTO
    # 1 = Finalizado

    def __str__(self):
        # Pra tentar mandar uma mensagem bonitinha tipo 'Comanda = 103'
        return "Comanda "+str(self.cod)
