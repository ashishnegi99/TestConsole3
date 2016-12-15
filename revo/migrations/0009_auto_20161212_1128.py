# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revo', '0008_auto_20161212_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='mac_id',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
