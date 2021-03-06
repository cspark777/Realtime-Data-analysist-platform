# Generated by Django 2.2.7 on 2020-05-14 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulations', '0018_step_definition_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='definition_type',
            field=models.CharField(choices=[('definition_schema', 'From Schema'), ('definition_json', 'JSON')], default='definition_schema', max_length=20, verbose_name='Event definition type'),
        ),
    ]
