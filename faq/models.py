# -*- coding: utf-8 -*-


from django.db import models


class FAQ(models.Model):
    faq_id = models.AutoField(
        primary_key=True,
    )
    title = models.TextField(
        verbose_name='Вопрос',
        blank=False, 
        null=True,
        db_column="faq_title",
    )
    answer = models.TextField(
        verbose_name='Ответ',
        blank=True,
        null=True,
        db_column="faq_answer",
    )
    date = models.DateField(
        verbose_name='Дата',
        blank=False,
        null=True,
        db_column="faq_date",
    )
    lang = models.CharField(
        max_length=2,
        blank=False,
        null=True,
        db_column="faq_lang",
    )
    position = models.IntegerField(
        default=0,
        blank=True,
        db_column="faq_position",
    )

    class Meta:
        ordering = ['position', 'pk']
        db_table = 'kase_faq'
        permissions = (
            ('view_faq', 'Can view faq'),
        )

    def __unicode__(self):
        return '%s' % self.title
