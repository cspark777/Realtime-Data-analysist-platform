# Generated by Django 2.2.7 on 2020-03-05 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('functions', '0004_auto_20200305_1028'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='functionendpoint',
            options={'ordering': ('id',), 'verbose_name': 'FunctionEndpoint', 'verbose_name_plural': 'FunctionEndpoint'},
        ),
    ]
