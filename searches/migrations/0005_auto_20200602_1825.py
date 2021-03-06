# Generated by Django 2.2.7 on 2020-06-02 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0010_stream_schema'),
        ('searches', '0004_auto_20200602_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='search',
            name='search_field',
            field=models.CharField(default='', max_length=200, verbose_name='Search Field'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='search',
            name='search_value',
            field=models.CharField(default='', max_length=200, verbose_name='Search Value'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='search',
            name='stream',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='streams.Stream'),
        ),
        migrations.AddField(
            model_name='search',
            name='time_window',
            field=models.CharField(default='1 hour', max_length=200, verbose_name='Time Window'),
        ),
        migrations.DeleteModel(
            name='SearchItem',
        ),
    ]
