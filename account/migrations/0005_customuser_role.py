# Generated by Django 2.2.7 on 2020-01-09 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_remove_customuser_developer_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('developer', 'Data Developer'), ('user', 'Data User')], max_length=9, null=True, verbose_name='Type'),
        ),
    ]
