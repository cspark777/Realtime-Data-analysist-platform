# Generated by Django 2.2.7 on 2020-01-27 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamprocessors', '0034_auto_20200124_0942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='streamprocessorstep',
            name='line_name',
        ),
        migrations.AddField(
            model_name='streamprocessorstep',
            name='event_field_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Event Field Name'),
        ),
    ]