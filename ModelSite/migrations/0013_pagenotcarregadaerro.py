# Generated by Django 5.0.3 on 2024-11-24 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ModelSite', '0012_alter_arquivo_id_cliente'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageNotCarregadaErro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token_referencia', models.CharField(max_length=255, unique=True)),
                ('error_type', models.CharField(max_length=100)),
                ('occurred_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
