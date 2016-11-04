# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20161011_1744'),
    ]

    operations = [
        migrations.RenameField(
            model_name='racktestresult',
            old_name='Script',
            new_name='TestJobExecutionId',
        ),
        migrations.RenameField(
            model_name='racktestresult',
            old_name='SuiteName2',
            new_name='TestJobName',
        ),
        migrations.AlterField(
            model_name='racktestresult',
            name='Date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='racktestresult',
            name='ExecutionTime',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
