# Generated by Django 4.1.3 on 2023-06-19 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0002_produto_tipo'),
        ('pedidos', '0002_pedido_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='observacao',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='produtos',
            field=models.ManyToManyField(blank=True, related_name='Produtos', to='produtos.produto'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='status',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='valor',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
