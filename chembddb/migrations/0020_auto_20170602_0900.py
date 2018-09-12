# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-02 09:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chembddb', '0019_auto_20170602_0534'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='verification',
        ),
        migrations.AddField(
            model_name='molgraph',
            name='verification',
            field=models.BooleanField(default=True, verbose_name='flag that tells us if the data is verified'),
        ),
    ]