# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revo', '0003_testsuite_mapping_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('mac_id', models.CharField(max_length=255)),
                ('serial_id', models.CharField(max_length=255)),
                ('device_type', models.CharField(max_length=255)),
                ('ip', models.GenericIPAddressField(protocol=b'IPv4')),
                ('router', models.CharField(max_length=255)),
            ],
        ),
    ]
