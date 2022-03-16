# Generated by Django 2.2.7 on 2020-06-12 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0016_auto_20200305_1028'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportitem',
            name='metric_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Metric Name'),
        ),
        migrations.AddField(
            model_name='reportitem',
            name='search_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Search Name'),
        ),
        migrations.AlterField(
            model_name='reportitem',
            name='type',
            field=models.TextField(blank=True, choices=[('data_table', 'Data Table'), ('saved_search', 'Saved Search'), ('bar_chart', 'Bar Chart'), ('histogram', 'Histogram'), ('series_chart', 'Time Series Chart'), ('scatter_plot', 'X/Y Scatter Plot'), ('metrics', 'Metrics'), ('summary', 'Summary'), ('external_source', 'External Source')], null=True, verbose_name='Type'),
        ),
    ]