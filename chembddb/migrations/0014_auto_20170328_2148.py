# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-28 21:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chembddb', '0013_auto_20170327_0614'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(blank=True, null=True)),
                ('comment', models.CharField(blank=True, max_length=256, verbose_name='if value is not a float/number')),
                ('met', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='chembddb.method')),
                ('mol_graph', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chembddb.MolGraph')),
                ('property', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='chembddb.MolProp')),
                ('publication', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='chembddb.Publication')),
            ],
        ),
        migrations.RemoveField(
            model_name='calcdata',
            name='met',
        ),
        migrations.RemoveField(
            model_name='calcdata',
            name='mol_graph',
        ),
        migrations.RemoveField(
            model_name='calcdata',
            name='property',
        ),
        migrations.RemoveField(
            model_name='expdata',
            name='mol_graph',
        ),
        migrations.RemoveField(
            model_name='expdata',
            name='property',
        ),
        migrations.RemoveField(
            model_name='expdata',
            name='publication',
        ),
        migrations.DeleteModel(
            name='calcdata',
        ),
        migrations.DeleteModel(
            name='ExpData',
        ),
    ]
