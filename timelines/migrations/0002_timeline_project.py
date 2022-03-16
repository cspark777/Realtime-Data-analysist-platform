# Generated by Django 2.2.7 on 2020-01-27 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_auto_20200117_1414'),
        ('timelines', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeline',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.Project'),
        ),
    ]
