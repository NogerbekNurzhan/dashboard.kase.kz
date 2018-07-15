# -*- coding: utf-8 -*-


from django.db import models


TRAND_TYPE_CHOICES = (
	("normal", "в изменении значения"),
	("percent", "в процентах"),
)


GRAPH_TYPE_CHOICES = (
	("linear", "линейный"),
	("bar", "столбики"),
	("arraychrt", "array"),
)


class FiniSection(models.Model):
	name_ru = models.CharField(
		verbose_name='Название [ru]',
		max_length=255,
		blank=False,
		null=True,
	)

	name_en = models.CharField(
		verbose_name='Название [en]',
		max_length=255,
		blank=True,
		null=True,
	)

	name_kz = models.CharField(
		verbose_name='Название [kz]',
		max_length=255,
		blank=True,
		null=True,
	)

	alt_ru = models.CharField(
		verbose_name='Подсказка [ru]',
		max_length=255,
		blank=True,
		null=True,
	)

	alt_en = models.CharField(
		verbose_name='Подсказка [en]',
		max_length=255,
		blank=True,
		null=True,
	)

	alt_kz = models.CharField(
		verbose_name='Подсказка [kz]',
		max_length=255,
		blank=True,
		null=True,
	)

	orderby = models.IntegerField(
		verbose_name='Поле для сортировки',
		default=0,
		blank=False,
		null=True,
	)

	isvisible = models.BooleanField(
		verbose_name='Отобразить',
		default=False,
		blank=False,
	)

	link = models.CharField(
		verbose_name='Ссылка',
		max_length=255,
		blank=True,
		null=True,
	)

	kase_info_key = models.CharField(
		verbose_name='Ключ',
		max_length=255,
		blank=True,
		null=True,
	)

	class Meta:
		ordering = ['orderby', 'pk']
		db_table = 'fini_section'
		permissions = (
            ('edit_section_of_indicators', 'Can edit section of indicators'),
        )

	def __unicode__(self):
		return '%s' % self.name_ru


class FiniCode(models.Model):
	section = models.ForeignKey(
		FiniSection,
		on_delete=models.CASCADE,
	)

	fini_code = models.CharField(
		verbose_name='Код',
		max_length=64,
		blank=False,
		null=True,
	)

	name_ru = models.CharField(
		verbose_name='Название [ru]',
		max_length=128,
		blank=False,
		null=True,
	)

	name_en = models.CharField(
		verbose_name='Название [en]',
		max_length=128,
		blank=True,
		null=True,
	)

	name_kz = models.CharField(
		verbose_name='Название [kz]',
		max_length=128,
		blank=True,
		null=True,
	)

	unit_ru = models.CharField(
		verbose_name='Единица измерения [ru]',
		max_length=100,
		blank=True,
		null=True,
	)

	unit_en = models.CharField(
		verbose_name='Единица измерения [en]',
		max_length=100,
		blank=True,
		null=True,
	)

	unit_kz = models.CharField(
		verbose_name='Единица измерения [kz]',
		max_length=100,
		blank=True,
		null=True,
	)

	title_ru = models.CharField(
		verbose_name='Подсказка [ru]',
		max_length=255,
		blank=True,
		null=True,
	)

	title_en = models.CharField(
		verbose_name='Подсказка [en]',
		max_length=255,
		blank=True,
		null=True,
	)

	title_kz = models.CharField(
		verbose_name='Подсказка [kz]',
		max_length=255,
		blank=True,
		null=True,
	)

	isvisible = models.BooleanField(
		verbose_name='Отобразить',
		default=False,
		blank=False,
	)

	fini_code_ind_ttl = models.IntegerField(
		verbose_name='Время жизни индикатора',
		blank=True,
		null=True,
	)

	fini_code_diff_ttl = models.IntegerField(
		verbose_name='Время жизни тренда',
		blank=True,
		null=True,
	)

	fini_code_so = models.IntegerField(
		verbose_name='Поле для сортировки',
		default=0,
		blank=False,
		null=True,
	)

	fini_code_chrt_type = models.CharField(
		verbose_name='График тип',
		max_length=20,
		choices=GRAPH_TYPE_CHOICES,
		blank=True,
		null=True,
	)

	fini_code_chrt_pd = models.IntegerField(
		verbose_name='График период',
		blank=True,
		null=True,
		default=0,
	)

	fini_code_ind_frmt = models.CharField(
		verbose_name='Разрядность индикатора',
		max_length=50,
		blank=True,
		null=True,
	)

	fini_code_diff_frmt = models.CharField(
		verbose_name='Разрядность тренда',
		max_length=50,
		blank=True,
		null=True,
	)

	trandtype = models.CharField(
		verbose_name='Выражение тренда',
		choices=TRAND_TYPE_CHOICES,
		max_length=20,
		blank=True,
		null=True,
	)

	link = models.CharField(
		verbose_name='Ссылка',
		max_length=255,
		blank=True,
		null=True,
	)

	kase_info_key = models.CharField(
		verbose_name='Ключ',
		max_length=255,
		blank=True,
		null=True,
	)

	value_divisor = models.IntegerField(
		verbose_name='Делитель',
		blank=True,
		null=True,
	)

	class Meta:
		ordering = ['fini_code_so', 'pk']
		db_table = 'fini_code'
		permissions = (
            ('view_indicators', 'Can view indicators'),
            ('edit_indicator', 'Can edit indicator'),
        )

	def __unicode__(self):
		return '%s. %s | %s' % (self.id, self.fini_code, self.name_ru)
