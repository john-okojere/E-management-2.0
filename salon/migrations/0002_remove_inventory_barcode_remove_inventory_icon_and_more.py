# Generated by Django 5.1.3 on 2024-11-29 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='barcode',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='icon',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='quantity',
        ),
    ]
