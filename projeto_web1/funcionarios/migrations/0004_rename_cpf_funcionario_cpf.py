# Generated by Django 4.1.3 on 2023-07-01 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('funcionarios', '0003_funcionario_user_alter_funcionario_telefone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='funcionario',
            old_name='CPF',
            new_name='cpf',
        ),
    ]
