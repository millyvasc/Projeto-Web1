from django.db import models

class Comanda(models.Model):
    cod = models.BigAutoField(primary_key=True) #BigAutoField, pra ser auto incrementável
    valorTotal = models.DecimalField(max_digits=10, decimal_places=2)
    mesa = models.IntegerField()

    def __str__(self):
        return "Comanda = "+self.cod #Pra tentar mandar uma mensagem bonitinha tipo 'Comanda = 103'