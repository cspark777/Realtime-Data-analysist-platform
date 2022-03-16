# Generated by Django 2.2.7 on 2020-06-01 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_auto_20200117_1414'),
        ('searches', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='search',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.Project'),
        ),
        migrations.AddField(
            model_name='searchitem',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.Project'),
        ),
    ]
