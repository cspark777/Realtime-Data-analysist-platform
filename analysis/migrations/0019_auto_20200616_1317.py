# Generated by Django 2.2.7 on 2020-06-16 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0018_reportitem_external_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reportitem',
            old_name='metric_name',
            new_name='kpi_metric',
        ),
        migrations.AddField(
            model_name='reportitem',
            name='kpi_category',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Metric Category'),
        ),
    ]
