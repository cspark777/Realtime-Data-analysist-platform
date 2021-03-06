# Generated by Django 2.2.7 on 2020-01-29 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datadictionaries', '0002_auto_20200129_1019'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_value', models.CharField(max_length=64, verbose_name='Source value')),
                ('mapped_value', models.CharField(max_length=64, verbose_name='Mapped value')),
                ('datadictionary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='datadictionaries.DataDictionary')),
            ],
        ),
    ]
