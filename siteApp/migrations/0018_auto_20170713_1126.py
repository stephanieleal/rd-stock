# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-13 14:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteApp', '0017_auto_20170710_0209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companynews',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 13, 11, 25, 58, 906499)),
        ),
        migrations.AlterField(
            model_name='companystockvalue',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 13, 11, 25, 58, 905609)),
        ),
    ]