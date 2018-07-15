# -*- coding: utf-8 -*-


from django.db import models
import reversion


@reversion.register(
    fields=(
        "meta_title",
        "meta_title_ru",
        "meta_title_en",
        "meta_title_kz",
        "head",
        "head_ru",
        "head_en",
        "head_kz",
        "body",
        "body_ru",
        "body_en",
        "body_kz",
        "slug",
        "is_public",
        "created_at",
        "updated_at",
    )
)
class StaticPage(models.Model):
    meta_title = models.CharField(
        verbose_name='Мета заголовок',
        max_length=255,
        blank=True,
        null=True,
    )

    head = models.CharField(
        verbose_name='Название страницы',
        max_length=255,
        blank=False,
    )

    slug = models.SlugField(
        verbose_name='ЧПУ',
        max_length=255,
        blank=True,
        null=True,
        unique=True
    )

    body = models.TextField(
        verbose_name='Тело страницы',
        blank=True,
        null=True,
    )

    is_public = models.BooleanField(
        verbose_name='Флаг публикации',
        default=False,
        blank=True,
    )

    idx = models.IntegerField(
        verbose_name='Поле для сортировки',
        default=0,
        blank=True,
    )

    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
        blank=True,
    )

    updated_at = models.DateTimeField(
        verbose_name='Дата обновления',
        auto_now=True,
        blank=True,
    )

    class Meta:
        ordering = ['idx', 'pk']
        db_table = 'kase_site_pages'
        permissions = (
            ('view_staticpage', 'Can view static pages'),
            ('view_staticpage_change_history', 'Can view change history of the static page'),
            ('revert_staticpage', 'Can revert static pages'),
        )

    def __unicode__(self):
        return '%s' % (self.head)
