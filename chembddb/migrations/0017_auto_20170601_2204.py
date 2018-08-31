# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-01 22:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chembddb', '0016_data_verification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unit',
            name='prop_name',
        ),
        migrations.RemoveField(
            model_name='data',
            name='unit',
        ),
        migrations.AddField(
            model_name='molprop',
            name='unit',
            field=models.CharField(default=' ', max_length=32, verbose_name='keyword for unit'),
        ),
        migrations.DeleteModel(
            name='Unit',
        ),
    ]
