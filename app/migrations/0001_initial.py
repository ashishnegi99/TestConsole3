# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appium',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('details', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Appium',
            },
        ),
        migrations.CreateModel(
            name='Revo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('SuiteName', models.CharField(max_length=30)),
                ('Test_Case', models.CharField(max_length=30)),
                ('FileName', models.CharField(max_length=30)),
                ('Total_Action', models.CharField(max_length=30)),
                ('Pass', models.CharField(max_length=30)),
                ('Fail', models.CharField(max_length=30)),
                ('Exe_Time', models.CharField(max_length=30)),
                ('Result', models.CharField(max_length=30)),
                ('create_date', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name_plural': 'Revo',
            },
        ),
        migrations.CreateModel(
            name='Set_Top_Box',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Device_Type', models.CharField(max_length=30)),
                ('IP_Adress', models.CharField(max_length=30)),
                ('Model_Name', models.CharField(max_length=30)),
                ('Serial_Number', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Set Top Box',
            },
        ),
        migrations.CreateModel(
            name='Storm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('details', models.TextField(blank=True)),
                ('date', models.DateTimeField()),
            ],
            options={
                'verbose_name_plural': 'Storm',
            },
        ),
    ]
