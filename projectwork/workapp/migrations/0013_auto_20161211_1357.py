# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-11 13:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workapp', '0012_auto_20161211_1336'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='username',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='collect',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 11, 13, 57, 0, 560902)),
        ),
        migrations.AlterField(
            model_name='houseinfo',
            name='housetype',
            field=models.CharField(choices=[('二室一厅一卫', '二室一厅一卫'), ('三室两厅两卫', '三室两厅两卫'), ('三室一厅两卫', '三室一厅两卫'), ('一室一厅一卫', '一室一厅一卫'), ('三室一厅一卫', '三室一厅一卫'), ('四室两厅两卫', '四室两厅两卫')], max_length=200),
        ),
    ]