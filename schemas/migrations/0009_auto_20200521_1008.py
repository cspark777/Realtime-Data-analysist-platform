# Generated by Django 2.2.7 on 2020-05-21 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schemas', '0008_auto_20200519_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schemafield',
            name='type_field',
            field=models.CharField(choices=[('string', 'String'), ('int', 'Integer'), ('float', 'Float'), ('boolean', 'Boolean'), ('date', 'Date')], default='string', max_length=10, verbose_name='Type Field'),
        ),
    ]
