# Generated by Django 4.0 on 2022-01-07 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants_site', '0003_restaurant_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='image',
            field=models.ImageField(upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
