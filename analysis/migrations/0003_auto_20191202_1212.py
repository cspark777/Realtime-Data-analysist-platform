# Generated by Django 2.2.7 on 2019-12-02 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0002_reportitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ('id',), 'verbose_name': 'Report', 'verbose_name_plural': 'Reports'},
        ),
        migrations.AlterModelOptions(
            name='reportitem',
            options={'ordering': ('id',), 'verbose_name': 'ReportItem', 'verbose_name_plural': 'ReportItems'},
        ),
        migrations.AddField(
            model_name='reportitem',
            name='expression',
            field=models.TextField(blank=True, null=True, verbose_name='Expression'),
        ),
        migrations.AddField(
            model_name='reportitem',
            name='filter',
            field=models.TextField(blank=True, null=True, verbose_name='Filter'),
        ),
        migrations.AddField(
            model_name='reportitem',
            name='limit',
            field=models.IntegerField(default=0, verbose_name='Limit'),
        ),
        migrations.AddField(
            model_name='reportitem',
            name='record_type',
            field=models.TextField(blank=True, null=True, verbose_name='Record Type'),
        ),
        migrations.AddField(
            model_name='reportitem',
            name='report',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='analysis.Report'),
        ),
        migrations.AddField(
            model_name='reportitem',
            name='x_value',
            field=models.TextField(blank=True, null=True, verbose_name='X Value'),
        ),
        migrations.AddField(
            model_name='reportitem',
            name='y_value',
            field=models.TextField(blank=True, null=True, verbose_name='Y Value'),
        ),
        migrations.AlterField(
            model_name='report',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='report',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='reportitem',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='reportitem',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='reportitem',
            name='type',
            field=models.TextField(blank=True, choices=[('report', 'report'), ('bar_chart', 'bar-chart'), ('line_chart', 'line-chart'), ('summary', 'summary')], null=True, verbose_name='Type'),
        ),
    ]
