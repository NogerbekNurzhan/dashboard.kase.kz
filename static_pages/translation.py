# -*- coding: utf-8 -*-


from modeltranslation.translator import TranslationOptions
from modeltranslation.translator import translator
from .models import StaticPage


class StaticPageTranslationOptions(TranslationOptions):
    fields = ('meta_title', 'head', 'body')


translator.register(StaticPage, StaticPageTranslationOptions)
