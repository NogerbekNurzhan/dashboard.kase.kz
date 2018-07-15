# -*- coding: utf-8 -*-


from django import forms
from .models import Video
from django_select2.forms import Select2Widget


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        exclude = ('idx',)
        widgets = {
            'category_id': Select2Widget,
        }

    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        self.fields['head'].widget.attrs = {
            'class': 'form-control',
            'id': 'head',
            'autocomplete': 'off',
        }
        self.fields['head_en'].widget.attrs = {
            'class': 'form-control',
            'id': 'head_en',
            'autocomplete': 'off',
        }
        self.fields['head_kz'].widget.attrs = {
            'class': 'form-control',
            'id': 'head_kz',
            'autocomplete': 'off',
        }
        self.fields['body'].widget.attrs = {
            'class': 'form-control custom-body-textarea',
            'id': 'body',
        }
        self.fields['body_en'].widget.attrs = {
            'class': 'form-control custom-body-textarea',
            'id': 'body_en',
        }
        self.fields['body_kz'].widget.attrs = {
            'class': 'form-control custom-body-textarea',
            'id': 'body_kz',
        }
        self.fields['link'].widget.attrs = {
            'class': 'form-control',
            'id': 'link',
            'autocomplete': 'off',
        }
        self.fields['link_en'].widget.attrs = {
            'class': 'form-control',
            'id': 'link_en',
            'autocomplete': 'off',
        }
        self.fields['link_kz'].widget.attrs = {
            'class': 'form-control',
            'id': 'link_kz',
            'autocomplete': 'off',
        }
        self.fields['category_id'].widget.attrs = {
            'class': 'form-control',
            'id': 'category_id',
        }
