# Generated by Django 2.2.7 on 2020-01-22 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamprocessors', '0028_auto_20200117_0727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streamprocessorstep',
            name='operator',
            field=models.CharField(blank=True, choices=[('sum', 'Sum'), ('count', 'Count'), ('min', 'Min'), ('max', 'Max'), ('average', 'Average')], max_length=20, null=True, verbose_name='Operator'),
        ),
    ]
