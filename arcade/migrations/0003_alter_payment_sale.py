# Generated by Django 5.1.3 on 2024-12-05 18:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arcade', '0002_remove_inventory_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='sale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arcade_payments', to='arcade.sale'),
        ),
    ]