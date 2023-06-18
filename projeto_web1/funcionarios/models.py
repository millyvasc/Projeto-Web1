from django.db import models

from django.db import models

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    CPF = models.CharField(max_length=14)
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=200)
    senha = models.CharField(max_length=100)
    tipo = models.IntegerField()

    def __str__(self):
        return self.nome

