# Generated by Django 2.2.7 on 2020-06-09 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_auto_20200609_0622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='cluster_type',
            field=models.CharField(default='Docker Swarm', max_length=256),
        ),
    ]
