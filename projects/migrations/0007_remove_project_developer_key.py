# Generated by Django 2.2.7 on 2020-01-10 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20200108_1343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='developer_key',
        ),
    ]
