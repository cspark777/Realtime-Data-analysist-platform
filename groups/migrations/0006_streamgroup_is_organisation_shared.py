# Generated by Django 2.2.7 on 2020-07-05 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("groups", "0005_auto_20200705_1332"),
    ]

    operations = [
        migrations.AddField(
            model_name="streamgroup",
            name="is_organisation_shared",
            field=models.BooleanField(default=False),
        ),
    ]