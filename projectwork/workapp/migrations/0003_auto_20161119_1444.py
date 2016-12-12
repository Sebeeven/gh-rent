# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-19 06:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workapp', '0002_auto_20161119_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='introduce',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='collect',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 19, 14, 44, 2, 906156)),
        ),
        migrations.AlterField(
            model_name='houseinfo',
            name='housetype',
            field=models.CharField(choices=[('二室一厅一卫', '二室一厅一卫'), ('三室两厅两卫', '三室两厅两卫'), ('四室两厅两卫', '四室两厅两卫'), ('一室一厅一卫', '一室一厅一卫'), ('三室一厅两卫', '三室一厅两卫'), ('三室一厅一卫', '三室一厅一卫')], max_length=200),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='sex',
            field=models.CharField(choices=[('保密', '保密'), ('男', '男'), ('女', '女')], default='保密', max_length=10),
        ),
    ]
