# Generated by Django 4.0.1 on 2024-12-17 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ModelSite', '0016_qrcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='SendEmailCliente',
            field=models.BooleanField(default=False),
        ),
    ]
