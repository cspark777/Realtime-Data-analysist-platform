# Generated by Django 2.2.7 on 2020-01-23 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamprocessors', '0030_streamprocessorstep_line_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='streamprocessorstep',
            name='percent',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Percent'),
        ),
        migrations.AlterField(
            model_name='streamprocessorstep',
            name='line_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Line Name'),
        ),
    ]
