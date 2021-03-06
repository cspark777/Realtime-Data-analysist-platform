# Generated by Django 2.2.7 on 2020-06-05 06:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collaboration', '0003_remove_collaboration_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='collaboration',
            name='email',
            field=models.EmailField(default='hello@data.com', max_length=254, verbose_name='email address'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='collaboration',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
