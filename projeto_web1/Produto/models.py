from django.db import models

class Produtos(models.Model):
    cod = models.CharField(max_length=20)
    nome = models.CharField(max_length=100)
    valorUnitario = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.CharField(max_length=200)
    estoque = models.IntegerField()

    def __str__(self):
        return self.nome
