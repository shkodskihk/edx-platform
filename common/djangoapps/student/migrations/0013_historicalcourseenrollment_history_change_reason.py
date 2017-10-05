# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0012_sociallink'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalcourseenrollment',
            name='history_change_reason',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
