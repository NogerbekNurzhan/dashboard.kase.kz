# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-04 07:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StaticPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True, verbose_name=b'\xd0\x9c\xd0\xb5\xd1\x82\xd0\xb0 \xd0\xb7\xd0\xb0\xd0\xb3\xd0\xbe\xd0\xbb\xd0\xbe\xd0\xb2\xd0\xbe\xd0\xba')),
                ('meta_title_ru', models.CharField(blank=True, max_length=255, null=True, verbose_name=b'\xd0\x9c\xd0\xb5\xd1\x82\xd0\xb0 \xd0\xb7\xd0\xb0\xd0\xb3\xd0\xbe\xd0\xbb\xd0\xbe\xd0\xb2\xd0\xbe\xd0\xba')),
                ('meta_title_en', models.CharField(blank=True, max_length=255, null=True, verbose_name=b'\xd0\x9c\xd0\xb5\xd1\x82\xd0\xb0 \xd0\xb7\xd0\xb0\xd0\xb3\xd0\xbe\xd0\xbb\xd0\xbe\xd0\xb2\xd0\xbe\xd0\xba')),
                ('meta_title_kz', models.CharField(blank=True, max_length=255, null=True, verbose_name=b'\xd0\x9c\xd0\xb5\xd1\x82\xd0\xb0 \xd0\xb7\xd0\xb0\xd0\xb3\xd0\xbe\xd0\xbb\xd0\xbe\xd0\xb2\xd0\xbe\xd0\xba')),
                ('head', models.CharField(max_length=255, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5 \xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x86\xd1\x8b')),
                ('head_ru', models.CharField(max_length=255, null=True, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5 \xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x86\xd1\x8b')),
                ('head_en', models.CharField(max_length=255, null=True, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5 \xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x86\xd1\x8b')),
                ('head_kz', models.CharField(max_length=255, null=True, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5 \xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x86\xd1\x8b')),
                ('body', models.TextField(blank=True, null=True, verbose_name=b'\xd0\xa2\xd0\xb5\xd0\xbb\xd0\xbe \xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x86\xd1\x8b')),
                ('body_ru', models.TextField(blank=True, null=True, verbose_name=b'\xd0\xa2\xd0\xb5\xd0\xbb\xd0\xbe \xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x86\xd1\x8b')),
                ('body_en', models.TextField(blank=True, null=True, verbose_name=b'\xd0\xa2\xd0\xb5\xd0\xbb\xd0\xbe \xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x86\xd1\x8b')),
                ('body_kz', models.TextField(blank=True, null=True, verbose_name=b'\xd0\xa2\xd0\xb5\xd0\xbb\xd0\xbe \xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x86\xd1\x8b')),
                ('is_public', models.BooleanField(default=False, verbose_name=b'\xd0\xa4\xd0\xbb\xd0\xb0\xd0\xb3 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8')),
                ('idx', models.IntegerField(blank=True, default=0, verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xbb\xd0\xb5 \xd0\xb4\xd0\xbb\xd1\x8f \xd1\x81\xd0\xbe\xd1\x80\xd1\x82\xd0\xb8\xd1\x80\xd0\xbe\xd0\xb2\xd0\xba\xd0\xb8')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd1\x81\xd0\xbe\xd0\xb7\xd0\xb4\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x8f')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbe\xd0\xb1\xd0\xbd\xd0\xbe\xd0\xb2\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f')),
            ],
            options={
                'ordering': ['idx', 'pk'],
                'db_table': 'kase_site_pages',
            },
        ),
    ]