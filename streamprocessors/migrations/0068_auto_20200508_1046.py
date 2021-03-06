# Generated by Django 2.2.7 on 2020-05-08 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamprocessors', '0067_streamprocessorstep_variable_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streamprocessorstep',
            name='steptype',
            field=models.CharField(choices=[('inbound', 'Inbound Event - Stream'), ('inboundtimer', 'Inbound Event - Timer Task'), ('inboundttp', 'Inbound Event - Load From API'), ('inboundkpi', 'Inbound Event - KPI Change'), ('outbound', 'Outbound Event - Stream'), ('outboundemail', 'Outbound Event - E-Mail'), ('outboundsms', 'Outbound Event - SMS'), ('outboundweb', 'Outbound Event - Web Hook'), ('function', 'Processor - Execute Function'), ('filter', 'Processor - Simple Filter'), ('select', 'Processor - Select Fields'), ('complex', 'Processor - Complex Filter'), ('map', 'Processor - Map Function'), ('map_event', 'Processor - Map Event To Event Type'), ('event', 'Processor - Create New Event Of Type'), ('lookup', 'Processor - Stream Lookup'), ('key', 'Processor - Record Key Performance Indicator'), ('workflow', 'Processor - Create Workflow Task'), ('sentiment', 'Processor - AWS Comprehend Sentiment Analysis'), ('transcribe', 'Processor - AWS Transcribe Task'), ('external', 'Processor - External API Call'), ('add', 'Processor - Add Or Update Field'), ('remove', 'Processor - Remove Field'), ('copy', 'Processor - Copy Field'), ('rename', 'Processor - Rename Field'), ('sum', 'Processor - Sum Field'), ('sleep', 'Processor - Sleep Step'), ('python', 'Processor - Python Step'), ('reset', 'Processor - Reset Timestamp'), ('dict', 'Processor - Data Dictionary Lookup & Replace'), ('adjust', 'Processor - Perform Calculation'), ('value', 'Processor - If Value In Set')], max_length=100, verbose_name='Type'),
        ),
    ]
