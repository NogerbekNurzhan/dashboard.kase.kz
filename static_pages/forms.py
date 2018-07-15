# -*- coding: utf-8 -*-


from django import forms
from .models import StaticPage


class StaticPageForm(forms.ModelForm):
    class Meta:
        model = StaticPage
        exclude = ('idx', 'created_at', 'updated_at')

    def __init__(self, user, *args, **kwargs):
        super(StaticPageForm, self).__init__(*args, **kwargs)
        self.fields['meta_title'].widget.attrs = {
            'class': 'form-control',
            'id': 'meta_title',
            'autocomplete': 'off',
        }
        self.fields['meta_title_en'].widget.attrs = {
            'class': 'form-control',
            'id': 'meta_title_en',
            'autocomplete': 'off',
        }
        self.fields['meta_title_kz'].widget.attrs = {
            'class': 'form-control',
            'id': 'meta_title_kz',
            'autocomplete': 'off',
        }
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
        self.fields['is_public'].widget.attrs = {
            'class': 'form-control',
            'id': 'is_public',
        }
        self.fields['slug'].widget.attrs = {
            'class': 'form-control',
            'id': 'slug',
            'autocomplete': 'off',
        }
        if user.user_permissions.filter(codename='use_wysiwyg_editor').exists():
            self.fields['body'].widget.attrs = {
                'class': 'body-summernote',
            }
            self.fields['body_en'].widget.attrs = {
                'class': 'body-summernote',
            }
            self.fields['body_kz'].widget.attrs = {
                'class': 'body-summernote',
            }
