# Generated by Django 4.2 on 2023-05-07 17:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipe", "0002_rename_food_recipe_recipe_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipe",
            name="owner",
            field=models.IntegerField(default=-1),
        ),
    ]