# Generated by Django 2.2.7 on 2020-03-05 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functions', '0006_functionendpoint_docker_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='functionendpoint',
            name='docker_image',
        ),
        migrations.AddField(
            model_name='function',
            name='docker_image',
            field=models.CharField(default='a', max_length=120, verbose_name='Docker Image'),
            preserve_default=False,
        ),
    ]
