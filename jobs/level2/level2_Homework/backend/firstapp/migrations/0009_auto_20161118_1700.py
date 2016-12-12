# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-18 09:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0008_auto_20161118_1645'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='password',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='choice',
            field=models.CharField(choices=[('dislike', 'dislike'), ('normal', 'normal'), ('like', 'like')], max_length=10),
        ),
    ]