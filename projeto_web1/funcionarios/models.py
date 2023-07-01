from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db import models

class Funcionario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    cpf = models.CharField(max_length=14)
    telefone = models.CharField(max_length=16)
    endereco = models.CharField(max_length=200)
    

    def __str__(self):
        return self.user.username
