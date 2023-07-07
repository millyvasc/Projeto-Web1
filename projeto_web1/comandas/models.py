from django.db import models


class Comanda(models.Model):
    # BigAutoField, pra ser auto incrementável
    cod = models.BigAutoField(primary_key=True)
    valorTotal = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    mesa = models.IntegerField()
    status = models.IntegerField(default=0)  # 0 = EM ABERTO
    # 1 = Finalizado
    opcaoPagamento = models.CharField(max_length=20, blank=True)
    trocoPara = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    
    #data = models.DateTimeField(blank=True)

    # dataCriacao = models.DateTimeField()
    # dataFechamento = models.DateTimeField()

    def __str__(self):
        # Pra tentar mandar uma mensagem bonitinha tipo 'Comanda = 103'
        return "Comanda "+str(self.cod)
