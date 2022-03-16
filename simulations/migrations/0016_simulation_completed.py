# Generated by Django 2.2.7 on 2020-04-30 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulations', '0015_simulation_is_running'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulation',
            name='completed',
            field=models.PositiveIntegerField(default=0, verbose_name='Completed, times'),
        ),
    ]