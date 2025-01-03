# Generated by Django 5.1.3 on 2024-11-26 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customuser_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(blank=True, choices=[('Cashier', 'Cashier'), ('Manager', 'Manager'), ('Waiter', 'Waiter'), ('IT Manager', 'IT Manager'), ('General Manager', 'General Manager'), ('Accountant', 'Accountant'), ('CEO', 'CEO')], max_length=50, null=True),
        ),
    ]
