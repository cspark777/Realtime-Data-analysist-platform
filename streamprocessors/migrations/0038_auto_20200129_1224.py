# Generated by Django 2.2.7 on 2020-01-29 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streamprocessors', '0037_auto_20200128_1428'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='streamprocessorstep',
            name='email',
        ),
        migrations.RemoveField(
            model_name='streamprocessorstep',
            name='telephone_number',
        ),
    ]
