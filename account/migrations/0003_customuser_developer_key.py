# Generated by Django 2.2.7 on 2019-12-24 09:35

from django.db import migrations, models
import secrets


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20191128_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='developer_key',
            field=models.CharField(default=secrets.token_hex, max_length=64, verbose_name='developer key'),
        ),
    ]
