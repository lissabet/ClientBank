# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-28 13:03
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InternetBanking', '0012_userskeys'),
    ]

    operations = [
        migrations.AddField(
            model_name='flatpay',
            name='Date',
            field=models.DateField(default=datetime.date(2017, 4, 28)),
        ),
        migrations.AddField(
            model_name='internetpay',
            name='Date',
            field=models.DateField(default=datetime.date(2017, 4, 28)),
        ),
        migrations.AddField(
            model_name='phoneoperation',
            name='Date',
            field=models.DateField(default=datetime.date(2017, 4, 28)),
        ),
    ]