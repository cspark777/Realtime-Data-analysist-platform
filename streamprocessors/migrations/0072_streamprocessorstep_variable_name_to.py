# Generated by Django 2.2.7 on 2020-05-15 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamprocessors', '0071_auto_20200514_0827'),
    ]

    operations = [
        migrations.AddField(
            model_name='streamprocessorstep',
            name='variable_name_to',
            field=models.CharField(blank=True, max_length=100, verbose_name='Variable Name'),
        ),
    ]
