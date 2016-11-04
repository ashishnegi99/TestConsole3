# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20161004_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revo',
            name='Exe_Time',
            field=models.TimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='revo',
            name='Fail',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='revo',
            name='Pass',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='revo',
            name='Total_Action',
            field=models.IntegerField(),
        ),
    ]
