# Generated by Django 5.1 on 2024-09-12 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("financeiro", "0013_alter_evento_participantes_selecionados"),
    ]

    operations = [
        migrations.AlterField(
            model_name="evento",
            name="participantes_selecionados",
            field=models.JSONField(blank=True, default=dict),
        ),
    ]