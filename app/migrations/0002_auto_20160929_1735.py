# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revo',
            name='Exe_Time',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='revo',
            name='Fail',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='revo',
            name='FileName',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='revo',
            name='Pass',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='revo',
            name='Result',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='revo',
            name='SuiteName',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='revo',
            name='Test_Case',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='revo',
            name='Total_Action',
            field=models.CharField(max_length=255),
        ),
    ]
