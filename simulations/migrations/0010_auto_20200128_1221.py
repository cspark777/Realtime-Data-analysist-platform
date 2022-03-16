# Generated by Django 2.2.7 on 2020-01-28 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulations', '0009_auto_20200128_0726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulation',
            name='run_count',
            field=models.PositiveIntegerField(default=1, verbose_name='Run Count'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='run_time',
            field=models.PositiveIntegerField(default=0, verbose_name='Run Time'),
        ),
    ]