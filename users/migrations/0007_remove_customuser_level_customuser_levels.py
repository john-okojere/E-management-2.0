# Generated by Django 5.1.3 on 2024-11-28 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_customuser_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='level',
        ),
        migrations.AddField(
            model_name='customuser',
            name='levels',
            field=models.CharField(choices=[(1, 1), (2, 2), (3, 3)], default=1, max_length=50),
        ),
    ]