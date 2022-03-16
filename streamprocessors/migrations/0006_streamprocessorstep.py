# Generated by Django 2.2.7 on 2019-11-27 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamprocessors', '0005_stream'),
    ]

    operations = [
        migrations.CreateModel(
            name='StreamProcessorStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('type', models.CharField(max_length=200)),
            ],
        ),
    ]
