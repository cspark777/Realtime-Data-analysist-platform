# Generated by Django 2.2.7 on 2020-06-09 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20200609_0549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='default_cluster_type',
            field=models.CharField(default='Docker Swarm', max_length=256),
        ),
    ]