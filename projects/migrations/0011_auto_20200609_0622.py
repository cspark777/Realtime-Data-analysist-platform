# Generated by Django 2.2.7 on 2020-06-09 06:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_auto_20200609_0550'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='default_cluster_endpoint',
            new_name='cluster_endpoint',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='default_cluster_type',
            new_name='cluster_type',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='default_druid_url',
            new_name='druid_url',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='default_kafka_url',
            new_name='kafka_url',
        ),
    ]
