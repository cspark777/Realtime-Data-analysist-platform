# Generated by Django 2.2.7 on 2020-06-01 12:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0008_auto_20200117_1414'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('streams', '0010_stream_schema'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('source_type', models.CharField(choices=[('TailCSV', 'Tail CSV'), ('TailJSON', 'Tail JSON'), ('S3', 'S3'), ('Kafka', 'Kafka')], max_length=200)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
                ('schema', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='streams.Stream')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
