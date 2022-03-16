# Generated by Django 2.2.7 on 2019-12-12 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
        ('simulations', '0003_auto_20191128_0902'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulation',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.Project'),
        ),
    ]
