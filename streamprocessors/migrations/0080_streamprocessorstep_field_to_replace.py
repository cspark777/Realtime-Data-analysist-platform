# Generated by Django 2.2.7 on 2020-07-13 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamprocessors', '0079_auto_20200710_0903'),
    ]

    operations = [
        migrations.AddField(
            model_name='streamprocessorstep',
            name='field_to_replace',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Replace Field Name'),
        ),
    ]
