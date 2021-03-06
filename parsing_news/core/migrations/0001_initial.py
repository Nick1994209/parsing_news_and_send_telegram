# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-28 11:29
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_series', models.FloatField(default=1, verbose_name=models.Model)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='Site address')),
            ],
        ),
        migrations.CreateModel(
            name='SiteTVSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_rus', models.CharField(blank=True, max_length=255)),
                ('name_eng', models.CharField(blank=True, max_length=255)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tv_series', to='core.Site')),
            ],
        ),
        migrations.CreateModel(
            name='TelegramBot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('name', models.CharField(blank=True, max_length=255)),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='core.TelegramBot')),
            ],
        ),
        migrations.CreateModel(
            name='UserSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dc', models.DateTimeField(auto_now_add=True)),
                ('serial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='core.SiteTVSeries')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='core.TelegramUser')),
            ],
        ),
        migrations.AddField(
            model_name='series',
            name='tv_series',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='series', to='core.SiteTVSeries'),
        ),
    ]
