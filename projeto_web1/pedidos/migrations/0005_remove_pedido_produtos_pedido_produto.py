# Generated by Django 4.1.3 on 2023-06-21 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0004_alter_produto_estoque_alter_produto_nome_and_more'),
        ('pedidos', '0004_alter_pedido_comanda'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='produtos',
        ),
        migrations.CreateModel(
            name='Pedido_Produto',
            fields=[
                ('cod', models.BigAutoField(primary_key=True, serialize=False)),
                ('cod_pedido', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='pedidos.pedido')),
                ('cod_produto', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='produtos.produto')),
            ],
        ),
    ]
