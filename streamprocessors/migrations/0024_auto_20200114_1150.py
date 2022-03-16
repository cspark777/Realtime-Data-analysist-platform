# Generated by Django 2.2.7 on 2020-01-14 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamprocessors', '0023_merge_20200114_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streamprocessorstep',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Recipient Email Address'),
        ),
        migrations.AlterField(
            model_name='streamprocessorstep',
            name='steptype',
            field=models.CharField(choices=[('inbound', 'Inbound Event - Stream'), ('outbound', 'Outbound Event - Stream'), ('outboundemal', 'Outbound Event - E-Mail'), ('outboundsms', 'Outbound Event - SMS'), ('outboundweb', 'Outbound Event - Web Hook'), ('filter', 'Processor - Simple Filter'), ('map', 'Processor - Map Function'), ('lookup', 'Processor - Record Lookup'), ('key', 'Processor - Record Key Performance Indicator'), ('workflow', 'Processor - Create Workflow Task'), ('sentiment', 'Processor - AWS Comprehend Sentiment Analysis'), ('transcribe', 'Processor - AWS Transcribe Task')], max_length=100, verbose_name='Type'),
        ),
    ]
