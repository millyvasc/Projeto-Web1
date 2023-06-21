# Generated by Django 4.1.3 on 2023-06-21 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0002_produto_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='descricao',
            field=models.CharField(max_length=200, verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='estoque',
            field=models.IntegerField(verbose_name='Quantidade em Estoque'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='nome',
            field=models.CharField(max_length=100, verbose_name='Nome do Produto'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='tipo',
            field=models.CharField(max_length=10, verbose_name='Tipo de Produto'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='valorUnitario',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor Unitário'),
        ),
    ]