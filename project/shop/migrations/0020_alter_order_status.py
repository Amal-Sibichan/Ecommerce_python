# Generated by Django 4.2.7 on 2023-12-15 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_order_pstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default='Pending', max_length=30),
        ),
    ]
