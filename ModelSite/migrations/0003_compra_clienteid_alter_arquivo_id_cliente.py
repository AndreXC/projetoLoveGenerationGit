# Generated by Django 5.0.3 on 2024-11-09 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ModelSite', '0002_arquivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='clienteId',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='arquivo',
            name='id_cliente',
            field=models.IntegerField(default=0),
        ),
    ]
