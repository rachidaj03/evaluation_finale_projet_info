# Generated by Django 4.2.4 on 2023-12-18 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashb", "0002_clie_statut_oppor"),
    ]

    operations = [
        migrations.AlterField(
            model_name="clie",
            name="statut_oppor",
            field=models.IntegerField(blank=True, db_column="statut_oppor", null=True),
        ),
    ]
