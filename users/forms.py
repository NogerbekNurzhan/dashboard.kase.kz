# -*- coding: utf-8 -*-


from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import Permission
from django.contrib import admin
from django.contrib.auth import password_validation


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_active', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {
            'class': 'form-control',
            'id': 'username',
        }
        self.fields['first_name'].widget.attrs = {
            'class': 'form-control',
            'id': 'first_name',
        }
        self.fields['last_name'].widget.attrs = {
            'class': 'form-control',
            'id': 'last_name',
        }
        self.fields['email'].widget.attrs = {
            'class': 'form-control',
            'id': 'email',
        }
        self.fields['password1'].widget.attrs = {
            'class': 'form-control',
            'id': 'password1',
        }
        self.fields['password2'].widget.attrs = {
            'class': 'form-control',
            'id': 'password2',
        }
        self.fields['is_active'].widget.attrs = {
            'class': 'form-control',
            'id': 'is_active',
        }


class UserEditForm(UserChangeForm):
    user_role = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=((0, _('Администатор')), (1, _('Модератор')), (2, _('Простой пользователь'))),
    )
    use_wysiwyg_editor = forms.BooleanField(
        required=False,
        label=_('Отобразить текстовой редактор (wysiwyg)'),
    )

    class Meta:
        model = User
        exclude = ('groups',)

    def __init__(self, *args, **kwargs):
        super(UserEditForm,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {
            'class': 'form-control',
            'id': 'username',
        }
        self.fields['first_name'].widget.attrs = {
            'class': 'form-control',
            'id': 'first_name',
        }
        self.fields['last_name'].widget.attrs = {
            'class': 'form-control',
            'id': 'last_name',
        }
        self.fields['email'].widget.attrs = {
            'class': 'form-control',
            'id': 'email',
        }
        self.fields['password'].widget.attrs = {
            'class': 'form-control',
            'id': 'password',
            'readonly': 'readonly',
            'disabled': 'disabled',
        }
        self.fields['is_active'].widget.attrs = {
            'class': 'form-control',
            'id': 'is_active',
        }
        self.fields['last_login'].widget.attrs = {
            'class': 'form-control',
            'id': 'last_login',
            'readonly': 'readonly',
        }
        self.fields['date_joined'].widget.attrs = {
            'class': 'form-control',
            'id': 'date_joined',
            'readonly': 'readonly',
        }
        self.fields['user_role'].widget.attrs = {
            'id': 'user_role',
        }
        self.fields['user_permissions'].widget.attrs = {
            'class': 'form-control',
            'id': 'user_permissions',
        }
        self.fields['user_permissions'].queryset = Permission.objects.filter(content_type__model__in=['slide', 'staticpage', 'user', 'document', 'video', 'finisection', 'finicode', 'event', 'faq']).exclude(codename='use_wysiwyg_editor')
        self.fields['user_permissions'].widget.choices = self.fields['user_permissions'].queryset.values_list('pk', 'name')


    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(_("Пользователь с такой электронной почтой уже существует."))
        return email


class UserPasswordChangeForm(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "new_password",
            }
        ),
        label=_("New password"),
        required=True,
    )

    def clean_new_password(self):
        password = self.cleaned_data.get('new_password')
        validate_password(password)
        return password
