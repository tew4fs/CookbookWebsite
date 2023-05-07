# Generated by Django 4.2 on 2023-05-07 17:29

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipe", "0003_recipe_owner"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="users",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(default=""), default=list, size=1000
            ),
        ),
    ]