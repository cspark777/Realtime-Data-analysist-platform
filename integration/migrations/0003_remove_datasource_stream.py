# Generated by Django 2.2.7 on 2020-06-02 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('integration', '0002_auto_20200602_0752'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datasource',
            name='stream',
        ),
    ]
