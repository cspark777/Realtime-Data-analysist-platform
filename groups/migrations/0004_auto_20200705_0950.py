# Generated by Django 2.2.7 on 2020-07-05 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0003_auto_20200705_0115'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulationgroup',
            name='sort_order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='streamgroup',
            name='sort_order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='streamprocessorgroup',
            name='sort_order',
            field=models.IntegerField(default=0),
        ),
    ]
