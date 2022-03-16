# Generated by Django 2.2.7 on 2020-06-08 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_organisation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='company_name',
        ),
        migrations.AddField(
            model_name='customuser',
            name='organisation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Organisation'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='organisation_owner',
            field=models.BooleanField(default=True),
        ),
    ]
