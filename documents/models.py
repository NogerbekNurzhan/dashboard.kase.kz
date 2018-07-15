# -*- coding: utf-8 -*-
 

from django.db import models
from closuretree.models import ClosureModel
from .validators import validate_file_extension
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
import datetime
from django.core.files.storage import FileSystemStorage
import transliterate
from CA.settings import DOCUMENT_FILE_STORAGE
 
 
CATEGORY_CHOICES = (
    (1, "Материалы СД"),
    (2, "Документы комитета СД"),
    (3, "Комитет по аудиту"),
    (4, "Комитет по стратегии"),
    (5, "Комитет по кадрам"),
    (7, "Планы, бюджеты, отчеты"),
    (8, "Документы, утвержденные СД"),
    (9, "Модернизация ИТ"),
    (11, "Листинговая комиссия"),
    (12, "Собрания акционеров"),
)
 
TAB_CHOICES = (
    (0, "По дате публикации"),
    (4, "Деятельность СВА"),
    (5, "Деятельность СУР"),
    (6, "Непроизводственного назначения"),
    (7, "Поручения СД")
)


DOCUMENT_STORAGE = FileSystemStorage(location=DOCUMENT_FILE_STORAGE)


def document_file_directory_path(instance, filename):
    if transliterate.detect_language(filename)=='ru':
        name, expansion = filename.split('.')
        file_name = transliterate.translit(name, reversed=True) + "." + expansion
    else:
        file_name = filename

    if instance.category=="1":
        path = 'files/bs_docs/' + str(datetime.datetime.now().year) + '/' + str('{:02d}'.format(datetime.datetime.now().month)) + '/' + '%s' % file_name
        return path
    elif instance.category=="2":
        path = 'files/comit_docs/' + '%s' % file_name
        return path
    elif instance.category=="3":
        path = 'files/comitet/audit/' + '%s' % file_name
        return path
    elif instance.category=="4":
        path = 'files/comitet/strategy/' + '%s' % file_name
        return path
    elif instance.category=="5":
        path = 'files/comitet/ethics/' + '%s' % file_name
        return path
    elif instance.category=="9":
        path = 'files/bs_docs/' + str(datetime.datetime.now().year) + '/' + str('{:02d}'.format(datetime.datetime.now().month)) + '/' + '%s' % file_name
        return path
    elif instance.category=="11":
        path = 'files/listing_docs/' + '%s' % file_name
        return path
    else:
        path = 'files/' + '%s' % file_name
        return path


class Document(ClosureModel):
    title = models.TextField(verbose_name='Название', blank=False, null=True)

    author_id = models.IntegerField(blank=True, null=True)
 
    date_add = models.DateTimeField(verbose_name='Дата публикации', blank=True, null=True)
 
    date_edit = models.DateTimeField(verbose_name='Дата обновления', auto_now=True, blank=True, null=True)
 
    src = models.FileField(max_length=255, storage=DOCUMENT_STORAGE, upload_to=document_file_directory_path, blank=True, null=True, validators=[validate_file_extension])
 
    filesize = models.IntegerField(editable=False, default=0, blank=True, null=True)
 
    category = models.IntegerField(verbose_name='Категория', choices=CATEGORY_CHOICES, db_column='type', blank=True, null=True)
 
    tab = models.IntegerField(verbose_name='Вкладка', choices=TAB_CHOICES, default=0, blank=False)

    position = models.IntegerField(verbose_name='Поле для сортировки', default=0, blank=True, null=True)

    parent = models.ForeignKey('self', related_name='children', null=True)

    del_field = models.BooleanField(db_column='del', default=False, blank=True)
 
    class Meta:
        ordering = ['position']
        db_table = 'kase_tree_docs'
        permissions = (
            ('view_document_1', 'Просмотр | "Материалы СД"'),
            ('add_document_1', 'Добавление | "Материалы СД"'),
            ('edit_document_1', 'Редактирование | "Материалы СД"'),
            ('delete_document_1', 'Удаление | "Материалы СД"'),
            ('change_order_document_1', 'Сохранение очередности | "Материалы СД"'),

            ('view_document_2', 'Просмотр | "Документы комитета СД"'),
            ('add_document_2', 'Добавление | "Документы комитета СД"'),
            ('edit_document_2', 'Редактирование | "Документы комитета СД"'),
            ('delete_document_2', 'Удаление | "Документы комитета СД"'),
            ('change_order_document_2', 'Сохранение очередности | "Документы комитета СД"'),

            ('view_document_3', 'Просмотр | "Комитет по аудиту"'),
            ('add_document_3', 'Добавление | "Комитет по аудиту"'),
            ('edit_document_3', 'Редактирование | "Комитет по аудиту"'),
            ('delete_document_3', 'Удаление | "Комитет по аудиту"'),
            ('change_order_document_3', 'Сохранение очередности | "Комитет по аудиту"'),

            ('view_document_4', 'Просмотр | "Комитет по стратегии"'),
            ('add_document_4', 'Добавление | "Комитет по стратегии"'),
            ('edit_document_4', 'Редактирование | "Комитет по стратегии"'),
            ('delete_document_4', 'Удаление | "Комитет по стратегии"'),
            ('change_order_document_4', 'Сохранение очередности | "Комитет по стратегии"'),

            ('view_document_5', 'Просмотр | "Комитет по кадрам"'),
            ('add_document_5', 'Добавление | "Комитет по кадрам"'),
            ('edit_document_5', 'Редактирование | "Комитет по кадрам"'),
            ('delete_document_5', 'Удаление | "Комитет по кадрам"'),
            ('change_order_document_5', 'Сохранение очередности | "Комитет по кадрам"'),

            ('view_document_7', 'Просмотр | "Планы, бюджеты, отчеты"'),
            ('add_document_7', 'Добавление | "Планы, бюджеты, отчеты"'),
            ('edit_document_7', 'Редактирование | "Планы, бюджеты, отчеты"'),
            ('delete_document_7', 'Удаление | "Планы, бюджеты, отчеты"'),
            ('change_order_document_7', 'Сохранение очередности | "Планы, бюджеты, отчеты"'),

            ('view_document_8', 'Просмотр | "Документы, утвержденные СД"'),
            ('add_document_8', 'Добавление | "Документы, утвержденные СД"'),
            ('edit_document_8', 'Редактирование | "Документы, утвержденные СД"'),
            ('delete_document_8', 'Удаление | "Документы, утвержденные СД"'),
            ('change_order_document_8', 'Сохранение очередности | "Документы, утвержденные СД"'),

            ('view_document_9', 'Просмотр | "Модернизация ИТ"'),
            ('add_document_9', 'Добавление | "Модернизация ИТ"'),
            ('edit_document_9', 'Редактирование | "Модернизация ИТ"'),
            ('delete_document_9', 'Удаление | "Модернизация ИТ"'),
            ('change_order_document_9', 'Сохранение очередности | "Модернизация ИТ"'),

            ('view_document_11', 'Просмотр | "Листинговая комиссия"'),
            ('add_document_11', 'Добавление | "Листинговая комиссия"'),
            ('edit_document_11', 'Редактирование | "Листинговая комиссия"'),
            ('delete_document_11', 'Удаление | "Листинговая комиссия"'),
            ('change_order_document_11', 'Сохранение очередности | "Листинговая комиссия"'),

            ('view_document_12', 'Просмотр | "Собрания акционеров"'),
            ('add_document_12', 'Добавление | "Собрания акционеров"'),
            ('edit_document_12', 'Редактирование | "Собрания акционеров"'),
            ('delete_document_12', 'Удаление | "Собрания акционеров"'),
            ('change_order_document_12', 'Сохранение очередности | "Собрания акционеров"'),
        )

    class ClosureMeta(object):
        parent_attr = 'parent'
 
    def __unicode__(self):
        return '%s' % (self.title)

    @classmethod
    def document_table_update(cls, parent_id, children, position=0):
        for child in children:
            cls.objects.filter(pk=child['id']).update(parent_id=parent_id, position=position)
            position = cls.document_table_update(child['id'], child.get('children', []), position+1)
        return position

    def childrens(self):
        if hasattr(self, '_cached_children'):
            children = self._toplevel().objects.filter(
                pk__in=[n.pk for n in self._cached_children]
            )
            children._result_cache = self._cached_children
            return children.filter(del_field=False).order_by('position')
        else:
            return self.get_descendants(include_self=False, depth=1)


@receiver(pre_save, sender=Document)
def delete_old_document_file(sender, instance, *args, **kwargs):
    if instance.pk:
        try:
            document = Document.objects.get(pk=instance.pk)
            if instance.src and document.src != instance.src:
                document.src.delete(False)
        except Document.DoesNotExist:
            pass
