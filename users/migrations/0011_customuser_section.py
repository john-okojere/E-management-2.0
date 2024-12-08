# Generated by Django 5.1.3 on 2024-11-28 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_remove_customuser_levels_alter_customuser_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='section',
            field=models.CharField(blank=True, choices=[('restaurant', 'Restaurant'), ('arcade', 'Arcade'), ('cosmetic_store', 'Cosmetic Store'), ('saloon', 'Saloon'), ('boutique', 'Boutique'), ('spa', 'Spa'), ('lounge', 'Lounge'), ('all', 'All')], default='none', max_length=50, null=True),
        ),
    ]
