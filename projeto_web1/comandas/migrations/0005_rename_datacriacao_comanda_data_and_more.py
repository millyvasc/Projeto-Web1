# Generated by Django 4.1.3 on 2023-07-05 22:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comandas', '0004_comanda_datacriacao_comanda_datafechamento'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comanda',
            old_name='dataCriacao',
            new_name='data',
        ),
        migrations.RemoveField(
            model_name='comanda',
            name='dataFechamento',
        ),
    ]
