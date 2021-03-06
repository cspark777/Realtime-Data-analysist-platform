# Generated by Django 2.2.7 on 2019-11-29 15:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('streamprocessors', '0008_auto_20191128_1724'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Stream',
        ),
        migrations.AddField(
            model_name='streamprocessorstep',
            name='streamprocessor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='streamprocessors.StreamProcessor'),
        ),
        migrations.AlterField(
            model_name='streamprocessor',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='streamprocessor',
            name='dsl',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='streamprocessor',
            name='invocations',
            field=models.IntegerField(default=0, verbose_name='Invocations'),
        ),
        migrations.AlterField(
            model_name='streamprocessor',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='streamprocessor',
            name='owning_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='streamprocessor',
            name='pub_date',
            field=models.DateTimeField(null=True, verbose_name='Date published'),
        ),
        migrations.AlterField(
            model_name='streamprocessor',
            name='status',
            field=models.IntegerField(default=0, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='streamprocessorstep',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='streamprocessorstep',
            name='steptype',
            field=models.CharField(max_length=200, verbose_name='Type'),
        ),
    ]
