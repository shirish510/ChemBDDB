# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-01 21:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chembddb', '0015_data_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='verification',
            field=models.BooleanField(default=True, verbose_name='flag that tells us if the data is verified'),
        ),
    ]