# Generated by Django 2.2.7 on 2020-02-03 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0008_auto_20200117_0727'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='display_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
