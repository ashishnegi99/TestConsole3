# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revo', '0012_auto_20161227_1524'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='enviournment',
            new_name='environment',
        ),
    ]
