# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-18 12:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0009_auto_20161118_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(null=True, upload_to='.'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='choice',
            field=models.CharField(choices=[('normal', 'normal'), ('like', 'like'), ('dislike', 'dislike')], max_length=10),
        ),
    ]