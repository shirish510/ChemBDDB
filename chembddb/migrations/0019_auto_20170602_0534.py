# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-02 05:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chembddb', '0018_delete_candidate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='comment',
        ),
        migrations.AddField(
            model_name='data',
            name='credit',
            field=models.CharField(default='The Hachmann Group', max_length=2256, verbose_name='username'),
        ),
        migrations.AddField(
            model_name='method',
            name='comment',
            field=models.CharField(blank=True, max_length=256, verbose_name='details for the method'),
        ),
    ]
