# Generated by Django 4.2.2 on 2023-07-08 12:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('comandas', '0008_comanda_opcaopagamento_comanda_trocopara'),
    ]

    operations = [
        migrations.AddField(
            model_name='comanda',
            name='data_e_hora',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
