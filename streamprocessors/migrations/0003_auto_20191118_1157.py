# Generated by Django 2.2.7 on 2019-11-18 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamprocessors', '0002_streamprocessor_dsl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streamprocessor',
            name='pub_date',
            field=models.DateTimeField(null=True, verbose_name='date published'),
        ),
    ]