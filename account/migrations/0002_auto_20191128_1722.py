# Generated by Django 2.2.7 on 2019-11-28 17:22

import account.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
                ('objects', account.models.UserManager()),
            ],
        ),
    ]