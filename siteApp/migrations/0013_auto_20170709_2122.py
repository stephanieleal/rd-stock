# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-10 00:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteApp', '0012_auto_20170709_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companynews',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 9, 21, 22, 28, 645492)),
        ),
        migrations.AlterField(
            model_name='companystockvalue',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 9, 21, 22, 28, 644607)),
        ),
    ]