# Generated by Django 5.1.3 on 2024-12-13 20:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Resturant', '0003_sale_table_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='description',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='image',
        ),
    ]
