# Generated by Django 2.2.7 on 2020-07-04 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulationgroup',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='streamgroup',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='streamprocessorgroup',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]