# Generated by Django 2.2.7 on 2020-01-28 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamprocessors', '0035_auto_20200127_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='streamprocessor',
            name='is_running',
            field=models.BooleanField(default=False, verbose_name='Running'),
        ),
    ]
