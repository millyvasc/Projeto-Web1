# Generated by Django 4.1.3 on 2023-06-18 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='tipo',
            field=models.CharField(default=2, max_length=10),
            preserve_default=False,
        ),
    ]
