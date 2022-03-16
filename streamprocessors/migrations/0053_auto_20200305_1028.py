# Generated by Django 2.2.7 on 2020-03-05 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamprocessors', '0052_streamprocessorstep_offset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streamprocessorstep',
            name='field_operation',
            field=models.CharField(blank=True, choices=[('+', 'Add To'), ('-', 'Substract From'), ('*', 'Multiple By'), ('/', 'Divide By')], max_length=100, null=True, verbose_name='Field Operation'),
        ),
        migrations.AlterField(
            model_name='streamprocessorstep',
            name='result_placement',
            field=models.CharField(blank=True, choices=[('aggregate', 'Aggregate Results'), ('join', 'Join Results To Inbound'), ('joininbound', 'Join Inbound To Results'), ('publish', 'Publish Onto Stream')], max_length=20, null=True, verbose_name='Result Placement'),
        ),
        migrations.AlterField(
            model_name='streamprocessorstep',
            name='steptype',
            field=models.CharField(choices=[('inbound', 'Inbound Event - Stream'), ('inboundtimer', 'Inbound Event - Timer Task'), ('inboundttp', 'Inbound Event - Load From API'), ('inboundkpi', 'Inbound Event - KPI Change'), ('outbound', 'Outbound Event - Stream'), ('outboundemail', 'Outbound Event - E-Mail'), ('outboundsms', 'Outbound Event - SMS'), ('outboundweb', 'Outbound Event - Web Hook'), ('filter', 'Processor - Simple Filter'), ('complex', 'Processor - Complex Filter'), ('map', 'Processor - Map Function'), ('lookup', 'Processor - Stream Lookup'), ('key', 'Processor - Record Key Performance Indicator'), ('workflow', 'Processor - Create Workflow Task'), ('sentiment', 'Processor - AWS Comprehend Sentiment Analysis'), ('transcribe', 'Processor - AWS Transcribe Task'), ('external', 'Processor - External API Call'), ('add', 'Processor - Add Field'), ('remove', 'Processor - Remove Field'), ('copy', 'Processor - Copy Field'), ('rename', 'Processor - Rename Field'), ('sum', 'Processor - Sum Field'), ('sleep', 'Processor - Sleep Step'), ('python', 'Processor - Python Step'), ('reset', 'Processor - Reset Timestamp'), ('dict', 'Processor - Data Dictionary Lookup & Replace'), ('adjust', 'Processor - Perform Calculation'), ('value', 'Processor - If Value In Set')], max_length=100, verbose_name='Type'),
        ),
    ]
