# Generated by Django 4.2.7 on 2023-12-07 03:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_address_home'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
