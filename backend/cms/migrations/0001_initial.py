# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-10-19 23:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('slug', models.CharField(max_length=60)),
                ('status', models.CharField(choices=[
                    ('publ', 'Public'),
                    ('priv', 'Private'),
                    ('arch', 'Archived')
                    ], max_length=4)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
