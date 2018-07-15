# -*- coding: utf-8 -*-


from django import forms
from .models import Slide
from django_select2.forms import Select2Widget
from .widgets import CustomClearableFileInput


class SlideForm(forms.ModelForm):
    class Meta:
        model = Slide
        exclude = ('idx',)
        widgets = {
            'location': Select2Widget,
            'image': CustomClearableFileInput,
        }

    def __init__(self, *args, **kwargs):
        super(SlideForm, self).__init__(*args, **kwargs)
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
        self.fields['opt_head'].widget.attrs = {
            'class': 'form-control',
            'id': 'opt_head',
            'autocomplete': 'off',
        }
        self.fields['opt_head_en'].widget.attrs = {
            'class': 'form-control',
            'id': 'opt_head_en',
            'autocomplete': 'off',
        }
        self.fields['opt_head_kz'].widget.attrs = {
            'class': 'form-control',
            'id': 'opt_head_kz',
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
        self.fields['location'].widget.attrs = {
            'class': 'form-control',
            'id': 'location',
        }
        self.fields['public'].widget.attrs = {
            'class': 'form-control',
            'id': 'public',
        }
        self.fields['image'].widget.attrs = {
            'accept': 'image/png, image/jpeg, image/gif',
            'id': 'image',
        }
        self.fields['url'].widget.attrs = {
            'class': 'form-control',
            'id': 'url',
            'autocomplete': 'off',
        }
        self.fields['url_en'].widget.attrs = {
            'class': 'form-control',
            'id': 'url_en',
            'autocomplete': 'off',
        }
        self.fields['url_kz'].widget.attrs = {
            'class': 'form-control',
            'id': 'url_kz',
            'autocomplete': 'off',
        }
