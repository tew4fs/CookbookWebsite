# Generated by Django 3.0.4 on 2020-03-28 00:33

import django.contrib.postgres.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='ingridients',
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=80), default="{}", size=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recipe',
            name='description',
            field=models.CharField(max_length=200),
        ),
    ]
