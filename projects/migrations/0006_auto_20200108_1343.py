# Generated by Django 2.2.7 on 2020-01-08 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streamprocessors', '0019_auto_20200108_1343'),
        ('streams', '0007_remove_stream_broker'),
        ('projects', '0005_auto_20200108_1114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='database',
            name='project',
        ),
        migrations.DeleteModel(
            name='Broker',
        ),
        migrations.DeleteModel(
            name='Database',
        ),
    ]
