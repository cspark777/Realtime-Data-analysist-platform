# Generated by Django 2.2.7 on 2020-02-10 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0010_auto_20200210_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportitem',
            name='filter_type',
            field=models.CharField(blank=True, choices=[('less_than', 'Less Than'), ('greater_than', 'Greater Than'), ('equal', 'Equal')], max_length=20, null=True, verbose_name='Filter type'),
        ),
    ]
