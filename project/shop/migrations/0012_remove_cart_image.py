# Generated by Django 4.2.7 on 2023-12-04 04:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_alter_cart_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='image',
        ),
    ]
