# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-10 17:45
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('InternetBanking', '0013_auto_20170428_1303'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransferMoneyAchive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AcceptUser', models.CharField(max_length=55)),
                ('Date', models.DateField(default=datetime.date(2017, 5, 10))),
                ('Amount', models.IntegerField()),
                ('UserId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='flatpay',
            name='Date',
            field=models.DateField(default=datetime.date(2017, 5, 10)),
        ),
        migrations.AlterField(
            model_name='internetpay',
            name='Date',
            field=models.DateField(default=datetime.date(2017, 5, 10)),
        ),
        migrations.AlterField(
            model_name='phoneoperation',
            name='Date',
            field=models.DateField(default=datetime.date(2017, 5, 10)),
        ),
    ]