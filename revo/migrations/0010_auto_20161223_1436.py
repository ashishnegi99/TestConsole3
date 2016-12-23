# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revo', '0009_auto_20161212_1128'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='testsuite',
            name='mapping_name',
        ),
        migrations.AddField(
            model_name='testsuite',
            name='cases',
            field=models.ManyToManyField(related_name='testcases', to='revo.TestCase'),
        ),
    ]
