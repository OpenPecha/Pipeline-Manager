# Generated by Django 3.2.15 on 2022-10-06 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipelines', '0004_auto_20221004_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='pipeline_config',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
