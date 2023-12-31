# Generated by Django 4.1.3 on 2023-06-21 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0003_alter_produto_descricao_alter_produto_estoque_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='estoque',
            field=models.IntegerField(verbose_name='Estoque'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='nome',
            field=models.CharField(max_length=100, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='tipo',
            field=models.CharField(max_length=10, verbose_name='Tipo'),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='', verbose_name='foto')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='produtos.produto', verbose_name='foto')),
            ],
            options={
                'verbose_name': 'foto',
                'verbose_name_plural': 'fotos',
                'ordering': ('pk',),
            },
        ),
    ]
