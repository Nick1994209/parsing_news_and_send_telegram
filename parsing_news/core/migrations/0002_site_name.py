# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-28 12:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
