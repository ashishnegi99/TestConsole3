# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revo', '0010_auto_20161223_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcase',
            name='name',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
