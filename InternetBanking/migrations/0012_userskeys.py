# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-26 17:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('InternetBanking', '0011_flatpay'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersKeys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Key1', models.CharField(max_length=10)),
                ('Key2', models.CharField(max_length=10)),
                ('Key3', models.CharField(max_length=10)),
                ('Key4', models.CharField(max_length=10)),
                ('Key5', models.CharField(max_length=10)),
                ('Key6', models.CharField(max_length=10)),
                ('Key7', models.CharField(max_length=10)),
                ('Key8', models.CharField(max_length=10)),
                ('Key9', models.CharField(max_length=10)),
                ('UserId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]