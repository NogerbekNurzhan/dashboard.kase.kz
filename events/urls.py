# -*- coding: utf-8 -*-


from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from .views import (
    EventLanguage,
    EventLanguageYear,
    EventCreateView,
    EventDeleteView,
    EventEditView,
    ImageDeleteView,
)


urlpatterns = [
    # "Event" | Language
    url(r'^(?P<language>[a-z]{2})/$',
        login_required(login_url=reverse_lazy('administration_login'))(EventLanguage.as_view()),
        name='event_language'),

    # "Event" | Language + Year
    url(r'^(?P<language>[a-z]{2})/(?P<year>[0-9]{4})/$',
        EventLanguageYear.as_view(),
        name='event_language_year'),

    # Event Create
    url(r'^(?P<language>[a-z]{2})/(?P<year>[0-9]{4})/create/$',
        EventCreateView.as_view(),
        name='event_create'),

    # Event Delete
    url(r'^(?P<language>[a-z]{2})/(?P<year>[0-9]{4})/(?P<pk>\d+)/delete/$',
        EventDeleteView.as_view(),
        name='event_delete'),

    # Event Edit
    url(r'^(?P<language>[a-z]{2})/(?P<year>[0-9]{4})/(?P<pk>\d+)/edit/$',
        EventEditView.as_view(),
        name='event_edit'),

    # Image Delete
    url(r'^(?P<pk>\d+)/image_delete/$',
        ImageDeleteView.as_view(),
        name='image_delete'),
]
