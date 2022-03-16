# Generated by Django 2.2.7 on 2020-02-18 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0013_auto_20200212_0646'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportitem',
            name='plot_type',
            field=models.CharField(blank=True, choices=[('events_over_time', 'Count Of Events Over Time'), ('events_over_time_cumulative', 'Count Of Events Over Time (Cumulative)'), ('value_from_report', 'A Value From The Event')], max_length=20, null=True, verbose_name='Plot type'),
        ),
    ]
