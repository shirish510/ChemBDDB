# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-27 06:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chembddb', '0011_auto_20170327_0441'),
    ]

    operations = [
        migrations.CreateModel(
            name='method',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(default='00000', max_length=32, verbose_name='Keyword for property')),
            ],
        ),
        migrations.AddField(
            model_name='calcdata',
            name='met',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='chembddb.method'),
        ),
    ]
