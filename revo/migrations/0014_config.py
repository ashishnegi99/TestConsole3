# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revo', '0013_auto_20161227_1615'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('loc_fix', models.CharField(max_length=255)),
                ('test_runner_path', models.CharField(max_length=255)),
                ('report_location', models.CharField(max_length=255)),
                ('run_path', models.CharField(max_length=255)),
                ('json_path', models.CharField(max_length=255)),
            ],
        ),
    ]
