# Generated by Django 2.2.7 on 2020-02-03 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamprocessors', '0041_auto_20200203_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='streamprocessorstep',
            name='timestamp_field_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Timestamp field name'),
        ),
    ]
