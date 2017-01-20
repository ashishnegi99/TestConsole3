# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revo', '0016_auto_20170106_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='testcase',
            name='mapping_name',
            field=models.CharField(default='simple', max_length=255),
            preserve_default=False,
        ),
    ]
