# Generated by Django 4.2.7 on 2023-12-04 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_remove_cart_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='cart_images/'),
        ),
    ]
