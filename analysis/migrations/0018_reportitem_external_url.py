# Generated by Django 2.2.7 on 2020-06-12 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0017_auto_20200612_2022'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportitem',
            name='external_url',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='External Url'),
        ),
    ]