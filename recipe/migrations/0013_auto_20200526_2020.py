# Generated by Django 3.0.3 on 2020-05-27 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0012_auto_20200514_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='cook_time',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='recipe',
            name='serves',
            field=models.IntegerField(default=0),
        ),
    ]
