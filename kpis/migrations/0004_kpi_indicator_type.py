# Generated by Django 2.2.7 on 2020-05-08 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpis', '0003_auto_20200204_0714'),
    ]

    operations = [
        migrations.AddField(
            model_name='kpi',
            name='indicator_type',
            field=models.CharField(choices=[('kpi_type_counter', 'Counter'), ('kpi_type_measurement', 'Measurement')], default='kpi_type_counter', max_length=30, verbose_name='Indicator Type'),
        ),
    ]
