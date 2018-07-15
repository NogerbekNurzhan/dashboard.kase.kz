# -*- coding: utf-8 -*-


from django import forms
from .models import Document
from .widgets import CustomClearableFileInput
from django_select2.forms import Select2Widget
from .validators import validate_domain_adress

class DocumentForm(forms.ModelForm):
    src_url = forms.URLField(label='Ссылка на файл', required=False, validators=[validate_domain_adress])

    class Meta:
        model = Document
        fields = ('title', 'src', 'tab', 'date_add')
        widgets = {
            'tab': Select2Widget,
            'src': CustomClearableFileInput,
        }

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs = {
            'class': 'form-control',
            'id': 'title',
            'style': 'resize:vertical;',
        }
        self.fields['src'].widget.attrs = {
            'accept':'.pdf, .zip, .rar, .doc, .docx, .rtf',
            'id': 'src',
        }
        self.fields['src_url'].widget.attrs = {
            'class': 'form-control',
            'id': 'src_url',
            'placeholder': 'http://doc.kase.kz/',
            'autocomplete': 'off',
        }
        self.fields['tab'].widget.attrs = {
            'class': 'form-control',
            'id': 'tab',
        }
        self.fields['date_add'].widget.attrs = {
            'class': 'form-control',
            'id': 'date_add',
            'readonly': 'readonly',
        }
        self.fields['date_add'].required = True 
