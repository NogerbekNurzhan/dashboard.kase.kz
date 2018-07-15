# -*- coding: utf-8 -*-


from django import forms
from .models import FiniSection, FiniCode
from django_select2.forms import Select2Widget


class FiniSectionForm(forms.ModelForm):
    class Meta:
        model = FiniSection
        exclude = ('orderby',)

    def __init__(self, *args, **kwargs):
        super(FiniSectionForm, self).__init__(*args, **kwargs)
        self.fields['name_ru'].widget.attrs = {
            'class': 'form-control',
            'id': 'name_ru',
            'autocomplete': 'off',
        }
        self.fields['name_en'].widget.attrs = {
            'class': 'form-control',
            'id': 'name_en',
            'autocomplete': 'off',
        }
        self.fields['name_kz'].widget.attrs = {
            'class': 'form-control',
            'id': 'name_kz',
            'autocomplete': 'off',
        }
        self.fields['alt_ru'].widget.attrs = {
            'class': 'form-control',
            'id': 'alt_ru',
            'autocomplete': 'off',
        }
        self.fields['alt_en'].widget.attrs = {
            'class': 'form-control',
            'id': 'alt_en',
            'autocomplete': 'off',
        }
        self.fields['alt_kz'].widget.attrs = {
            'class': 'form-control',
            'id': 'alt_kz',
            'autocomplete': 'off',
        }
        self.fields['isvisible'].widget.attrs = {
            'class': 'form-control',
            'id': 'isvisible',
        }
        self.fields['link'].widget.attrs = {
            'class': 'form-control',
            'id': 'link',
            'autocomplete': 'off',
        }
        self.fields['kase_info_key'].widget.attrs = {
            'class': 'form-control',
            'id': 'kase_info_key',
            'autocomplete': 'off',
        }


class FiniCodeForm(forms.ModelForm):
    class Meta:
        model = FiniCode
        exclude = ('fini_code_so', 'section',)
        widgets = {
            'fini_code_chrt_type': Select2Widget,
            'trandtype': Select2Widget,
            'fini_code_ind_frmt': forms.NumberInput,
            'fini_code_diff_frmt': forms.NumberInput,
        }

    def __init__(self, *args, **kwargs):
        super(FiniCodeForm, self).__init__(*args, **kwargs)
        self.fields['fini_code'].widget.attrs = {
            'class': 'form-control',
            'id': 'fini_code',
            'autocomplete': 'off',
        }
        self.fields['name_ru'].widget.attrs = {
            'class': 'form-control',
            'id': 'name_ru',
            'autocomplete': 'off',
        }
        self.fields['name_en'].widget.attrs = {
            'class': 'form-control',
            'id': 'name_en',
            'autocomplete': 'off',
        }
        self.fields['name_kz'].widget.attrs = {
            'class': 'form-control',
            'id': 'name_kz',
            'autocomplete': 'off',
        }
        self.fields['unit_ru'].widget.attrs = {
            'class': 'form-control',
            'id': 'unit_ru',
            'autocomplete': 'off',
        }
        self.fields['unit_en'].widget.attrs = {
            'class': 'form-control',
            'id': 'unit_en',
            'autocomplete': 'off',
        }
        self.fields['unit_kz'].widget.attrs = {
            'class': 'form-control',
            'id': 'unit_kz',
            'autocomplete': 'off',
        }
        self.fields['title_ru'].widget.attrs = {
            'class': 'form-control',
            'id': 'title_ru',
            'autocomplete': 'off',
        }
        self.fields['title_en'].widget.attrs = {
            'class': 'form-control',
            'id': 'title_en',
            'autocomplete': 'off',
        }
        self.fields['title_kz'].widget.attrs = {
            'class': 'form-control',
            'id': 'title_kz',
            'autocomplete': 'off',
        }
        self.fields['isvisible'].widget.attrs = {
            'class': 'form-control',
            'id': 'isvisible',
        }
        self.fields['fini_code_ind_ttl'].widget.attrs = {
            'class': 'form-control',
            'id': 'fini_code_ind_ttl',
            'autocomplete': 'off',
        }
        self.fields['fini_code_diff_ttl'].widget.attrs = {
            'class': 'form-control',
            'id': 'fini_code_diff_ttl',
            'autocomplete': 'off',
        }
        self.fields['fini_code_chrt_type'].widget.attrs = {
            'class': 'form-control',
            'id': 'fini_code_chrt_type',
        }
        self.fields['fini_code_chrt_pd'].widget.attrs = {
            'class': 'form-control',
            'id': 'fini_code_chrt_pd',
            'autocomplete': 'off',
        }
        self.fields['fini_code_ind_frmt'].widget.attrs = {
            'class': 'form-control',
            'id': 'fini_code_ind_frmt',
            'autocomplete': 'off',
        }
        self.fields['fini_code_diff_frmt'].widget.attrs = {
            'class': 'form-control',
            'id': 'fini_code_diff_frmt',
            'autocomplete': 'off',
        }
        self.fields['trandtype'].widget.attrs = {
            'class': 'form-control',
            'id': 'trandtype',
        }
        self.fields['link'].widget.attrs = {
            'class': 'form-control',
            'id': 'link',
            'autocomplete': 'off',
        }
        self.fields['kase_info_key'].widget.attrs = {
            'class': 'form-control',
            'id': 'kase_info_key',
            'autocomplete': 'off',
        }
        self.fields['value_divisor'].widget.attrs = {
            'class': 'form-control',
            'id': 'value_divisor',
            'autocomplete': 'off',
        }
