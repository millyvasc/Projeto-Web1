# Generated by Django 4.1.3 on 2023-07-01 03:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('funcionarios', '0002_remove_funcionario_nome_remove_funcionario_senha_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionario',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='telefone',
            field=models.CharField(max_length=16),
        ),
    ]
