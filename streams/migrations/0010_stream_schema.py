# Generated by Django 2.2.7 on 2020-02-15 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schemas', '0001_initial'),
        ('streams', '0009_stream_display_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='schema',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='schemas.Schema'),
        ),
    ]
