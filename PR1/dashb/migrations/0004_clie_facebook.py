# Generated by Django 4.2.4 on 2023-12-19 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashb", "0003_alter_clie_statut_oppor"),
    ]

    operations = [
        migrations.AddField(
            model_name="clie",
            name="facebook",
            field=models.IntegerField(blank=True, db_column="facebook", null=True),
        ),
    ]
