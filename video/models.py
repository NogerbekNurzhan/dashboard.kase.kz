# -*- coding: utf-8 -*-


from django.db import models


CATEGORY_CHOICES = (
    (1, "Фондовый рынок статус PRO"),
)


class Video(models.Model):
	head = models.CharField(
		verbose_name='Заголовок',
		max_length=200,
		blank=False,
		null=False,
	)

	body = models.TextField(
		verbose_name='Описание',
		blank=True,
		null=True,
	)

	link = models.URLField(
		verbose_name='Cсылка',
		max_length=200,
		blank=False,
		null=False,
	)

	category_id = models.IntegerField(
		verbose_name='Категория',
		choices=CATEGORY_CHOICES,
		blank=False,
		null=False,
	)

	idx = models.IntegerField(
		verbose_name='Поле для сортировки',
		default=0,
		blank=True,
		null=True,
	)

	date_create = models.DateTimeField(auto_now_add=True)

	date_update = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['idx', 'pk']
		db_table = 'kase_video'
		permissions = (
			('view_video', 'Can view videos'),
		)

	def __unicode__(self):
		return '%s' % (self.head)
