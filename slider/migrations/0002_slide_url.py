# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-05 06:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slider', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='slide',
            name='url',
            field=models.URLField(blank=True, null=True, verbose_name=b'C\xd1\x81\xd1\x8b\xd0\xbb\xd0\xba\xd0\xb0'),
        ),
    ]
