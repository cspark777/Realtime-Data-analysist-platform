# Generated by Django 2.2.7 on 2020-06-07 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamprocessors', '0073_auto_20200521_0900'),
    ]

    operations = [
        migrations.AddField(
            model_name='workflowtask',
            name='type',
            field=models.CharField(choices=[('information', 'Information'), ('warning', 'Warning'), ('alert', 'Alert')], default='information', max_length=100, verbose_name='Task Type'),
        ),
    ]
