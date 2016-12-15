# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20161014_1753'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Revo',
        ),
        migrations.DeleteModel(
            name='Set_Top_Box',
        ),
        migrations.DeleteModel(
            name='Test_Suite',
        ),
    ]
