# Generated by Django 4.1.3 on 2023-06-19 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comandas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comanda',
            name='status',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]