# Generated by Django 3.0.3 on 2020-05-12 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_verified'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Verified',
            new_name='Unverified',
        ),
    ]
