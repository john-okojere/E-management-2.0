# Generated by Django 5.1.3 on 2024-12-17 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Resturant', '0007_inventory_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='day',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
