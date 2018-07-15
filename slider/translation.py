# -*- coding: utf-8 -*-


from modeltranslation.translator import TranslationOptions
from modeltranslation.translator import translator
from .models import Slide


class SlideTranslationOptions(TranslationOptions):
    fields = ('head', 'opt_head', 'body', 'url',)


translator.register(Slide, SlideTranslationOptions)
