# Generated by Django 4.2.7 on 2023-12-03 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='cart_images/'),
        ),
    ]
