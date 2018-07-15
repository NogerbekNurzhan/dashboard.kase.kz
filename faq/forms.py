# -*- coding: utf-8 -*-


from django import forms
from .models import FAQ


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        exclude = ('faq_id', 'lang', 'position',)

    def __init__(self, *args, **kwargs):
        super(FAQForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs = {
            'class': 'form-control custom-body-textarea',
            'id': 'title',
        }
        self.fields['answer'].widget.attrs = {
            'class': 'form-control custom-body-textarea',
            'id': 'answer',
        }
        self.fields['date'].widget.attrs = {
            'class': 'form-control',
            'id': 'date',
            'autocomplete': 'off',
            'readonly': 'readonly',
        }
