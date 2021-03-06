# Generated by Django 2.2.7 on 2020-01-08 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamprocessors', '0019_auto_20200108_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streamprocessorstep',
            name='steptype',
            field=models.CharField(choices=[('inbound', 'Inbound Event - Stream'), ('outbound', 'Outbound Event - Stream'), ('outboundemal', 'Outbound Event - E-Mail'), ('outboundsms', 'Outbound Event - SMS'), ('outboundweb', 'Outbound Event - Web Hook'), ('filter', 'Processor - Simple Filter'), ('map', 'Processor - Map Function'), ('lookup', 'Processor - Record Lookup'), ('key', 'Processor - Record Key Performance Indicator'), ('workflow', 'Processor - Create Workflow Task'), ('sentiment', 'Processor - AWS Comprehend Sentiment Analysis')], max_length=8, verbose_name='Type'),
        ),
    ]
