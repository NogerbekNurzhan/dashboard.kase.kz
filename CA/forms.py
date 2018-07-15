# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate


class AdministrationAuthenticationForm(AuthenticationForm):
    """
        A custom authentication form used in the administration application.
    """
    def __init__(self, *args, **kwargs):
        super(AdministrationAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {
            'class': 'form-control',
        }
        self.fields['password'].widget.attrs = {
            'class': 'form-control',
        }

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                _("This account is inactive."),
                code='inactive',
            )
