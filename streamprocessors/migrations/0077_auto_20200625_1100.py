# Generated by Django 2.2.7 on 2020-06-25 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('streamprocessors', '0076_auto_20200616_1930'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='streamprocessorstep',
            name='subtype',
        ),
        migrations.AlterField(
            model_name='streamprocessorstep',
            name='streamprocessor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='streamprocessors.StreamProcessor'),
        ),
    ]
