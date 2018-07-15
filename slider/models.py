# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
import reversion


LOCATION_CHOICES = (
    (1, "Главная страница"),
    (2, "Страница мероприятий"),
)


# Model "Slide"
@reversion.register(
    fields=(
        "head",
        "head_ru",
        "head_en",
        "head_kz",
        "opt_head",
        "opt_head_ru",
        "opt_head_en",
        "opt_head_kz",
        "body",
        "body_ru",
        "body_en",
        "body_kz",
        "location",
        "public",
        "image",
        "url",
        "url_ru",
        "url_en",
        "url_kz",
    )
)
class Slide(models.Model):
    head = models.CharField(
        verbose_name='Заголовок',
        max_length=200,
        blank=False,
    )

    opt_head = models.CharField(
        verbose_name='Опциональный заголовок',
        max_length=200,
        blank=True,
        null=True,
    )

    body = models.TextField(
        verbose_name='Описание',
        blank=False,
    )

    location = models.IntegerField(
        verbose_name='Местоположение слайда',
        choices=LOCATION_CHOICES,
        blank=False,
    )

    public = models.BooleanField(
        verbose_name='Опубликован',
        default=False,
        blank=True,
    )

    idx = models.IntegerField(
        verbose_name='Поле для сортировки',
        default=0,
        blank=True,
    )

    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='slider/images/%Y/%m/%d/',
        blank=False,
    )

    url = models.URLField(
        verbose_name='Cсылка',
        max_length=200,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['idx', 'pk']
        db_table = 'kase_slider'
        permissions = (
            ('view_slide', 'Can view slides'),
            ('view_slide_change_history', 'Can view change history of the slide'),
            ('revert_slide', 'Can revert slides'),
        )

    def __unicode__(self):
        return '%s | %s (%s)' % (self.head, self.opt_head, self.get_location_display())


@receiver(pre_save, sender=Slide)
def delete_old_slide_image(sender, instance, *args, **kwargs):
    if instance.pk:
        try:
            slide = Slide.objects.get(pk=instance.pk)
            if instance.image and slide.image != instance.image:
                slide.image.delete(False)
        except Slide.DoesNotExist:
            pass
