# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revo', '0004_device'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='device_type',
            field=models.CharField(default=b'VM', max_length=255, choices=[(b'VM', b'VM'), (b'IPC', b'IPC'), (b'MKB', b'MKB')]),
        ),
        migrations.AlterField(
            model_name='device',
            name='mac_id',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
