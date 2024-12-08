# Generated by Django 5.1.3 on 2024-12-06 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arcade', '0004_alter_payment_sale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
        migrations.AlterField(
            model_name='saleitem',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
    ]