# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0003_scheduleconfig'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduleconfig',
            name='deliver_verified_deadline_reminder',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='scheduleconfig',
            name='enqueue_verified_deadline_reminder',
            field=models.BooleanField(default=False),
        ),
    ]
