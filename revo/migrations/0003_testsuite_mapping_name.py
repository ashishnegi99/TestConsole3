# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revo', '0002_auto_20161117_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='testsuite',
            name='mapping_name',
            field=models.CharField(default='default', max_length=255),
            preserve_default=False,
        ),
    ]
