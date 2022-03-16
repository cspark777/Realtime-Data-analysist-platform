# Generated by Django 2.2.7 on 2019-12-09 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0005_auto_20191206_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportitem',
            name='type',
            field=models.TextField(blank=True, choices=[('data_table', 'data_table'), ('bar_chart', 'bar_chart'), ('line_chart', 'line_chart'), ('summary', 'summary')], null=True, verbose_name='Type'),
        ),
    ]
