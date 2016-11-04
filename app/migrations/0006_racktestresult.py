# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20161010_1615'),
    ]

    operations = [
        migrations.CreateModel(
            name='racktestresult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('idTestResult', models.IntegerField()),
                ('Date', models.DateTimeField(default=datetime.datetime.now)),
                ('ProjectName', models.CharField(max_length=255)),
                ('SuiteName', models.CharField(max_length=255)),
                ('TestCaseID', models.CharField(max_length=255)),
                ('SuiteName2', models.CharField(max_length=255)),
                ('Script', models.CharField(max_length=255)),
                ('Author', models.CharField(max_length=255)),
                ('Tester', models.CharField(max_length=255)),
                ('BoxType', models.CharField(max_length=255)),
                ('BoxUnitAddress', models.IntegerField()),
                ('BoxIP', models.CharField(max_length=255)),
                ('TotalActions', models.IntegerField()),
                ('TotalConditions', models.IntegerField()),
                ('PassNumbers', models.IntegerField()),
                ('FailNumbers', models.IntegerField()),
                ('Result', models.CharField(max_length=255)),
                ('ExecutionTime', models.TimeField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Rack Test Result',
            },
        ),
    ]
