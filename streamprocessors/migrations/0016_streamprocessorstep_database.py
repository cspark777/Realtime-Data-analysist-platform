# Generated by Django 2.2.7 on 2019-12-16 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_broker_database'),
        ('streamprocessors', '0015_streamprocessor_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='streamprocessorstep',
            name='database',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.Database'),
        ),
    ]