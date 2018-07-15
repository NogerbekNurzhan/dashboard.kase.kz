# -*- coding: utf-8 -*-


import os
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_file_extension(value):
    extension = os.path.splitext(value.name)[1] 
    valid_extensions = ['.pdf', '.doc', '.docx', '.rtf', '.zip', '.rar']
    if not extension.lower() in valid_extensions:
        raise ValidationError(_('Файл с данным расширением недоступен для загрузки.'))

def validate_domain_adress(value):
	if 'doc.kase.kz' not in value:
		raise ValidationError(_('Неправильное доменное имя. Вы можете ссылаться лишь на файлы по адресу http://doc.kase.kz/'))
