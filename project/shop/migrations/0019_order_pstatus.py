# Generated by Django 4.2.7 on 2023-12-10 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='pstatus',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
