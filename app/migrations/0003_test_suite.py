# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20160929_1735'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test_Suite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Test_Suite_Name', models.CharField(max_length=100)),
            ],
        ),
    ]
