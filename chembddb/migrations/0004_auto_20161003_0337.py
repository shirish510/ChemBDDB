# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-03 03:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chembddb', '0003_auto_20161003_0310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expdata',
            name='publication',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='chembddb.Publication'),
        ),
    ]
