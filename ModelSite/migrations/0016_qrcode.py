# Generated by Django 5.0.3 on 2024-12-15 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ModelSite', '0015_compra'),
    ]

    operations = [
        migrations.CreateModel(
            name='Qrcode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token_referencia', models.CharField(max_length=255, unique=True)),
                ('qrcode', models.BinaryField(blank=True)),
            ],
        ),
    ]
