# Generated by Django 2.2.7 on 2019-12-02 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamprocessors', '0011_streamprocessorstep_ordering'),
    ]

    operations = [
        migrations.AddField(
            model_name='streamprocessorstep',
            name='broker',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Broker'),
        ),
        migrations.AddField(
            model_name='streamprocessorstep',
            name='category_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Category name'),
        ),
        migrations.AddField(
            model_name='streamprocessorstep',
            name='expression',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='Expression'),
        ),
        migrations.AddField(
            model_name='streamprocessorstep',
            name='field',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Field'),
        ),
        migrations.AddField(
            model_name='streamprocessorstep',
            name='filter_value',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='Filter Value'),
        ),
        migrations.AddField(
            model_name='streamprocessorstep',
            name='lookup_field',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Lookup field'),
        ),
        migrations.AddField(
            model_name='streamprocessorstep',
            name='lookup_value',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Lookup Value'),
        ),
        migrations.AddField(
            model_name='streamprocessorstep',
            name='metric',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Metric'),
        ),
        migrations.AddField(
            model_name='streamprocessorstep',
            name='record',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Record'),
        ),
        migrations.AddField(
            model_name='streamprocessorstep',
            name='record_type',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Record Type'),
        ),
        migrations.AddField(
            model_name='streamprocessorstep',
            name='subtype',
            field=models.CharField(blank=True, choices=[('kafka', 'Kafka'), ('google', 'Google Pubsub')], max_length=100, null=True, verbose_name='SubType'),
        ),
        migrations.AddField(
            model_name='streamprocessorstep',
            name='time_period',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Time Period'),
        ),
        migrations.AddField(
            model_name='streamprocessorstep',
            name='topic',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Topic'),
        ),
        migrations.AddField(
            model_name='streamprocessorstep',
            name='value',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Value'),
        ),
        migrations.AlterField(
            model_name='streamprocessorstep',
            name='steptype',
            field=models.CharField(choices=[('inbound', 'Inbound Message'), ('outbound', 'Outbound Message'), ('filter', 'Simple Filter'), ('map', 'Map'), ('lookup', 'Record Lookup'), ('key', 'Record Key Performance Indicator')], max_length=8, verbose_name='Type'),
        ),
    ]
