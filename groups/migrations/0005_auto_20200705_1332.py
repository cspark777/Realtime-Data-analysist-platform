# Generated by Django 2.2.7 on 2020-07-05 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0004_auto_20200705_0950'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='simulationgroup',
            options={'ordering': ('sort_order',), 'verbose_name': 'Simulation Groups', 'verbose_name_plural': 'Simulation Groups'},
        ),
        migrations.AlterModelOptions(
            name='streamgroup',
            options={'ordering': ('sort_order',), 'verbose_name': 'Stream Group', 'verbose_name_plural': 'Stream Groups'},
        ),
        migrations.AlterModelOptions(
            name='streamprocessorgroup',
            options={'ordering': ('sort_order',), 'verbose_name': 'Stream Processor Group', 'verbose_name_plural': 'Stream Processor Groups'},
        ),
        migrations.AlterField(
            model_name='simulationgroup',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='streamgroup',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='streamprocessorgroup',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AddConstraint(
            model_name='simulationgroup',
            constraint=models.UniqueConstraint(fields=('project', 'name'), name='unique_project_simulation_group'),
        ),
        migrations.AddConstraint(
            model_name='streamgroup',
            constraint=models.UniqueConstraint(fields=('project', 'name'), name='unique_project_stream_group'),
        ),
        migrations.AddConstraint(
            model_name='streamprocessorgroup',
            constraint=models.UniqueConstraint(fields=('project', 'name'), name='unique_project_streamprocessor_group'),
        ),
    ]
