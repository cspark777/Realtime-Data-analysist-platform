# Generated by Django 2.2.7 on 2020-05-07 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamprocessors', '0063_auto_20200507_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streamprocessorstep',
            name='result_placement',
            field=models.CharField(blank=True, choices=[('aggregate', 'Aggregate Resultss and Add to Event'), ('join', 'Join Results To Inbound'), ('joininbound', 'Join Inbound To Results'), ('replace', 'Replace Inbound Event With Results')], max_length=20, null=True, verbose_name='Result Placement'),
        ),
    ]
