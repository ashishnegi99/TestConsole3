# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('revo', '0005_auto_20161122_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='ip',
            field=models.GenericIPAddressField(validators=[django.core.validators.validate_ipv46_address]),
        ),
    ]
