# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-12 03:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('line_server', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linetext',
            name='line_num',
            field=models.IntegerField(db_index=True, default=0),
        ),
    ]