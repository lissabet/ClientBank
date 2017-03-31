# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 18:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ClientBank', '0002_userinformation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CurrencyName', models.CharField(max_length=100)),
                ('CurrencyCode', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AccountNumber', models.CharField(max_length=25)),
                ('ContractNumber', models.CharField(max_length=10)),
                ('CurrencyId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ClientBank.Currency')),
            ],
        ),
        migrations.CreateModel(
            name='ProductStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StatusName', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TypeName', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='products',
            name='StatusId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ClientBank.ProductStatus'),
        ),
        migrations.AddField(
            model_name='products',
            name='TypeId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ClientBank.ProductType'),
        ),
    ]