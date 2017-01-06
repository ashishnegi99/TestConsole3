# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revo', '0015_auto_20161228_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='environment',
            field=models.ForeignKey(related_name='devices', to='revo.Config'),
        ),
        migrations.AlterField(
            model_name='testsuite',
            name='cases',
            field=models.ManyToManyField(related_name='testsuites', to='revo.TestCase'),
        ),
    ]
