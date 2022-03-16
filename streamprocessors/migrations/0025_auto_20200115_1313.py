# Generated by Django 2.2.7 on 2020-01-15 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamprocessors', '0024_auto_20200114_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='streamprocessorstep',
            name='column_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Column Name'),
        ),
        migrations.AddField(
            model_name='streamprocessorstep',
            name='key_type',
            field=models.CharField(blank=True, choices=[('from_event', 'A Value From Event'), ('static_value', 'A Static Value')], max_length=20, null=True, verbose_name='Key Type'),
        ),
        migrations.AddField(
            model_name='streamprocessorstep',
            name='key_value',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Key Value'),
        ),
        migrations.AddField(
            model_name='streamprocessorstep',
            name='operator',
            field=models.CharField(blank=True, choices=[('sum', 'Sum'), ('count', 'Count'), ('min', 'Min'), ('max', 'Max')], max_length=20, null=True, verbose_name='Operator'),
        ),
        migrations.AddField(
            model_name='streamprocessorstep',
            name='result_placement',
            field=models.CharField(blank=True, choices=[('aggregate', 'Aggregate Results'), ('join', 'Join Results To Inbound'), (('joininbound', 'Join Inbound To Results'), 'publish', 'Publish Onto Stream')], max_length=20, null=True, verbose_name='Result Placement'),
        ),
        migrations.AddField(
            model_name='streamprocessorstep',
            name='stream',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Publish Onto Stream'),
        ),
        migrations.AddField(
            model_name='streamprocessorstep',
            name='time_window',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Time Window'),
        ),
    ]
