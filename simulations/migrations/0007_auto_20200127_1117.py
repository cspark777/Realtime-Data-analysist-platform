# Generated by Django 2.2.7 on 2020-01-27 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulations', '0006_auto_20200120_0944'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='step',
            name='delay',
        ),
        migrations.AddField(
            model_name='step',
            name='delay_type',
            field=models.CharField(choices=[('static', 'Static Value'), ('random', 'Random Value')], default='static', max_length=100, verbose_name='Delay Type'),
        ),
        migrations.AddField(
            model_name='step',
            name='random_value',
            field=models.FloatField(default=0, verbose_name='Random Value'),
        ),
        migrations.AddField(
            model_name='step',
            name='static_value',
            field=models.FloatField(default=0, verbose_name='Static Value'),
        ),
    ]