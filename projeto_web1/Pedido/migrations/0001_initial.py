# Generated by Django 4.1.3 on 2023-06-15 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Produto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('cod', models.BigAutoField(max_length=20, primary_key=True, serialize=False)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('observacao', models.CharField(max_length=200)),
                ('produtos', models.ManyToManyField(related_name='Produtos', to='Produto.produto')),
            ],
        ),
    ]