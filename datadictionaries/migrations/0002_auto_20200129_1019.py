# Generated by Django 2.2.7 on 2020-01-29 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datadictionaries', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datadictionary',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='datadictionary',
            name='name',
            field=models.CharField(max_length=32, verbose_name='Name'),
        ),
    ]
