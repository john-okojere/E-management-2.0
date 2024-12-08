# Generated by Django 5.1.3 on 2024-11-28 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_customuser_levels_customuser_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='levels',
            field=models.CharField(default='1', max_length=55),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='level',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3')], default=1, max_length=50),
        ),
    ]
