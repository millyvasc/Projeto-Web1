from django.db import models


class Produto(models.Model):

    cod = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100, verbose_name='Nome')
    valorUnitario = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Valor Unitário')
    descricao = models.CharField(max_length=200, verbose_name='Descrição')
    estoque = models.IntegerField(verbose_name='Estoque')
    tipo = models.CharField(max_length=10, verbose_name='Tipo')
    img = models.ImageField('img', upload_to='')

    def __str__(self):
        return self.nome