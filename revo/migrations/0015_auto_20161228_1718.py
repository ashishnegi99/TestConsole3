# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revo', '0014_config'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='environment',
            field=models.ForeignKey(related_name='environment', to='revo.Config'),
        ),
    ]
