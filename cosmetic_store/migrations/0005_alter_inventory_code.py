# Generated by Django 5.1.3 on 2024-12-08 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cosmetic_store', '0004_remove_inventory_description_remove_inventory_icon_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='code',
            field=models.CharField(max_length=100),
        ),
    ]
