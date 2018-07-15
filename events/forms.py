# -*- coding: utf-8 -*-


from django import forms
from .models import Event


class EventCreateForm(forms.ModelForm):
    image_field = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'multiple': True,
                'accept': 'image/png, image/jpeg, image/gif',
                'id': 'image_field',
            }
        ),
        required=False
    )

    class Meta:
        model = Event
        exclude = ('event_id', 'event_removed', 'event_lang',)

    def __init__(self, user, *args, **kwargs):
        super(EventCreateForm, self).__init__(*args, **kwargs)
        self.fields['event_title'].widget.attrs = {
            'class': 'form-control',
            'id': 'event_title',
            'autocomplete': 'off',
        }
        self.fields['event_shortname'].widget.attrs = {
            'class': 'form-control',
            'id': 'event_shortname',
            'autocomplete': 'off',
        }
        self.fields['event_body'].widget.attrs = {
            'class': 'form-control custom-body-textarea',
            'id': 'body',
        }
        self.fields['event_active'].widget = forms.CheckboxInput()
        self.fields['event_active'].widget.attrs = {
            'class': 'form-control',
            'id': 'event_active',
        }
        self.fields['event_date'].widget.attrs = {
            'class': 'form-control',
            'id': 'event_date',
            'readonly': 'readonly',
        }
        if user.user_permissions.filter(codename='use_wysiwyg_editor').exists():
            self.fields['event_body'].widget.attrs = {
                'class': 'body-summernote',
            }


class EventEditForm(forms.ModelForm):
    image_field = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'multiple': True,
                'accept': 'image/png, image/jpeg, image/gif',
                'id': 'image_field',
            }
        ),
        required=False
    )

    class Meta:
        model = Event
        exclude = ('event_id', 'event_removed', 'event_lang',)

    def __init__(self, user, *args, **kwargs):
        super(EventEditForm, self).__init__(*args, **kwargs)
        self.fields['event_title'].widget.attrs = {
            'class': 'form-control',
            'id': 'event_title',
            'autocomplete': 'off',
        }
        self.fields['event_shortname'].widget.attrs = {
            'class': 'form-control',
            'id': 'event_shortname',
            'autocomplete': 'off',
            'readonly': 'readonly',
        }
        self.fields['event_body'].widget.attrs = {
            'class': 'form-control custom-body-textarea',
            'id': 'body',
        }
        self.fields['event_active'].widget = forms.CheckboxInput()
        self.fields['event_active'].widget.attrs = {
            'class': 'form-control',
            'id': 'event_active',
        }
        self.fields['event_date'].widget.attrs = {
            'class': 'form-control',
            'id': 'event_date',
            'autocomplete': 'off',
            'readonly': 'readonly',
        }
        if user.user_permissions.filter(codename='use_wysiwyg_editor').exists():
            self.fields['event_body'].widget.attrs = {
                'class': 'body-summernote',
            }
