# Generated by Django 2.2.7 on 2020-05-14 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streamprocessors', '0070_auto_20200514_0821'),
    ]

    operations = [
        migrations.RenameField(
            model_name='streamprocessorstep',
            old_name='event_field_name_new',
            new_name='event_field_name_from',
        ),
        migrations.RenameField(
            model_name='streamprocessorstep',
            old_name='key_type_new',
            new_name='key_type_from',
        ),
        migrations.RenameField(
            model_name='streamprocessorstep',
            old_name='static_value_new',
            new_name='static_value_from',
        ),
        migrations.RenameField(
            model_name='streamprocessorstep',
            old_name='variable_name_new',
            new_name='variable_name_from',
        ),
    ]
