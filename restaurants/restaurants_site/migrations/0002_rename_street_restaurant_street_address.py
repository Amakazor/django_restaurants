# Generated by Django 4.0 on 2022-01-03 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants_site', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurant',
            old_name='street',
            new_name='street_address',
        ),
    ]
