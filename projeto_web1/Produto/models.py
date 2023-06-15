from django.db import models

class Produtos(models.Model):

    cod = models.BigAutoField(max_length=20, primary_key=True) #BigAutoField, pra ser auto incrementável
    nome = models.CharField(max_length=100)
    valorUnitario = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.CharField(max_length=00)
    estoque = models.IntegerField()

    def __str__(self):
        return self.nome
