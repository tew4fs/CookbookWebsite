# Generated by Django 3.0.3 on 2020-05-14 17:49

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0011_auto_20200419_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='users',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(default=-1), default=list, size=1000),
        ),
    ]
