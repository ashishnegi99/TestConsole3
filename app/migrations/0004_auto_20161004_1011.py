# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_test_suite'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='test_suite',
            options={'verbose_name_plural': 'Test Suite'},
        ),
    ]
