# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-19 21:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20160819_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='myprofile',
            name='favourite_pizza',
            field=models.CharField(default='pepperoni', max_length=5, verbose_name='favourite pizza'),
            preserve_default=False,
        ),
    ]
