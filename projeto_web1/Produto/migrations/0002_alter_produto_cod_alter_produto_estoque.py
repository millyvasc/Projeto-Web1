# Generated by Django 4.1.3 on 2023-06-15 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Produto', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='cod',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='produto',
            name='estoque',
            field=models.IntegerField(),
        ),
    ]
