# Generated by Django 2.2.7 on 2020-02-05 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamprocessors', '0043_auto_20200203_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='streamprocessorstep',
            name='data_dictionary_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Data dictionary name'),
        ),
        migrations.AddField(
            model_name='streamprocessorstep',
            name='dictionary_field_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Dictionary field name'),
        ),
        migrations.AlterField(
            model_name='streamprocessorstep',
            name='steptype',
            field=models.CharField(choices=[('inbound', 'Inbound Event - Stream'), ('inboundtimer', 'Inbound Event - Timer Task'), ('inboundttp', 'Inbound Event - Load From HTTP Source'), ('outbound', 'Outbound Event - Stream'), ('outboundemail', 'Outbound Event - E-Mail'), ('outboundsms', 'Outbound Event - SMS'), ('outboundweb', 'Outbound Event - Web Hook'), ('filter', 'Processor - Simple Filter'), ('map', 'Processor - Map Function'), ('lookup', 'Processor - Stream Lookup'), ('key', 'Processor - Record Key Performance Indicator'), ('workflow', 'Processor - Create Workflow Task'), ('sentiment', 'Processor - AWS Comprehend Sentiment Analysis'), ('transcribe', 'Processor - AWS Transcribe Task'), ('external', 'Processor - External API Call'), ('manipulate', 'Processor - Manipulate Fields'), ('sleep', 'Processor - Sleep Step'), ('python', 'Processor - Python Step'), ('reset', 'Processor - Reset Timestamp'), ('dict', 'Processor - Data Dictionary Lookup & Replace')], max_length=100, verbose_name='Type'),
        ),
    ]