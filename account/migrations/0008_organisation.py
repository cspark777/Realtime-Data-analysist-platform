# Generated by Django 2.2.7 on 2020-06-08 08:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_customuser_developer_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invite_key', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('company_name', models.CharField(max_length=200, verbose_name='company name')),
                ('default_DRUID_URL', models.CharField(blank=True, max_length=256, null=True)),
                ('default_CLUSTER_TYPE', models.CharField(blank=True, max_length=256, null=True)),
                ('default_CLUSTER_ENDPOINT', models.CharField(blank=True, max_length=256, null=True)),
                ('default_KAFKA_URL', models.CharField(blank=True, max_length=256, null=True)),
            ],
        ),
    ]