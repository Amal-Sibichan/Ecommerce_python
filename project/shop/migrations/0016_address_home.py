# Generated by Django 4.2.7 on 2023-12-07 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_alter_order_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='home',
            field=models.CharField(default=1, max_length=55),
            preserve_default=False,
        ),
    ]
