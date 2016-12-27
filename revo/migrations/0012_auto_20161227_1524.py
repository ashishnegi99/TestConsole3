# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('revo', '0011_auto_20161223_1457'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='mac_id',
            new_name='terminal_id',
        ),
        migrations.RenameField(
            model_name='device',
            old_name='serial_id',
            new_name='unit_address',
        ),
        migrations.AddField(
            model_name='device',
            name='client_ip',
            field=models.GenericIPAddressField(blank=True, null=True, validators=[django.core.validators.validate_ipv46_address]),
        ),
        migrations.AddField(
            model_name='device',
            name='enviournment',
            field=models.CharField(default=b'SIT', max_length=255),
        ),
        migrations.AlterField(
            model_name='device',
            name='device_type',
            field=models.CharField(default=b'VM', max_length=255, choices=[(b'VMS', b'VMS'), (b'IMG', b'IMG'), (b'IPC2', b'IPC2'), (b'MKB', b'MKB')]),
        ),
        migrations.AlterField(
            model_name='device',
            name='host',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='device',
            name='router',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
