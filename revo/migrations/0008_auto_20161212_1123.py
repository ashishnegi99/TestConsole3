# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('revo', '0007_device_host'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='host',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='ip',
            field=models.GenericIPAddressField(blank=True, null=True, validators=[django.core.validators.validate_ipv46_address]),
        ),
        migrations.AlterField(
            model_name='device',
            name='mac_id',
            field=models.CharField(unique=True, max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='name',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
