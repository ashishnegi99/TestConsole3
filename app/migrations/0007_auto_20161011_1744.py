# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_racktestresult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='racktestresult',
            name='BoxUnitAddress',
            field=models.CharField(max_length=255),
        ),
    ]
