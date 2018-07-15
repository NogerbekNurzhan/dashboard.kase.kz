# -*- coding: utf-8 -*-


from django.db import models


class Event(models.Model):
    event_id = models.AutoField(
        primary_key=True,
    )

    event_title = models.TextField(
        verbose_name='Название события',
        blank=False, 
        null=True,
    )

    event_shortname = models.CharField(
        verbose_name='Адрес',
        max_length=255,
        blank=False,
        null=True,
    )

    event_date = models.DateField(
        verbose_name='Дата события',
        blank=False,
        null=True,
    )

    event_body = models.TextField(
        verbose_name='Описание события',
        blank=True,
        null=True,
    )

    event_active = models.NullBooleanField(
        verbose_name='Публиковать',
        default=False,
        blank=False,
        null=True,
    )

    event_removed = models.NullBooleanField(
        default=False,
        blank=False,
        null=True,
    )

    event_lang = models.CharField(
        max_length=2,
        blank=False,
        null=True,
    )


    class Meta:
        ordering = ['pk']
        db_table = 'kase_events'
        permissions = (
            ('view_events', 'Can view events'),
        )

    def __unicode__(self):
        return '%s' % self.event_title
