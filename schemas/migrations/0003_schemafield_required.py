# Generated by Django 2.2.7 on 2020-03-04 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schemas', '0002_auto_20200223_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='schemafield',
            name='required',
            field=models.BooleanField(default=False, verbose_name='Required'),
        ),
    ]
