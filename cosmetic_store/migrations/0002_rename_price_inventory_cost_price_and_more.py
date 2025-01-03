# Generated by Django 5.1.3 on 2024-11-28 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cosmetic_store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventory',
            old_name='price',
            new_name='cost_price',
        ),
        migrations.AddField(
            model_name='inventory',
            name='selling_price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
    ]
