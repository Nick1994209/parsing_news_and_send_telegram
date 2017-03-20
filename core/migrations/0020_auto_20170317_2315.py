# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-17 20:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20170317_2040'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('rss', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='core.Rss')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rss', to='core.TelegramUser')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='userrss',
            unique_together=set([('user', 'rss')]),
        ),
    ]
