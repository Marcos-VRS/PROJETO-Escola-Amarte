# Generated by Django 5.1 on 2024-10-08 14:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("financeiro", "0018_financeiro_cadastro_valor_pago"),
    ]

    operations = [
        migrations.AddField(
            model_name="financeiro_cadastro",
            name="data_de_pagamento",
            field=models.CharField(
                default="05",
                max_length=2,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Deve conter apenas 2 números entre 01 e 31.",
                        regex="^([0-9]{1,2})$",
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="financeiro_cadastro",
            name="frequencia_de_pagamento",
            field=models.CharField(
                choices=[
                    ("Avulso", "Avulso"),
                    ("Aula", "Aula"),
                    ("Mensalidade", "Mensalidade"),
                ],
                max_length=50,
            ),
        ),
    ]
