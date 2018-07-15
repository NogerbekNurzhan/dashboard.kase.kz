# -*- coding: utf-8 -*-


from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from .views import (
    SectionListView,
    SectionEditView,
    IndicatorEditView,
    SectionSortingView,
    IndicatorSortingView,
)


urlpatterns = [
    # Section List
    url(r'^$',
        login_required(login_url=reverse_lazy('administration_login'))(SectionListView.as_view()),
        name='section_list'),

    # Section Edit
    url(r'^(?P<pk>\d+)/section_edit/$',
        SectionEditView.as_view(),
        name='section_edit'),

    # Indicator Edit
    url(r'^(?P<pk>\d+)/indicator_edit/$',
        IndicatorEditView.as_view(),
        name='indicator_edit'),

    # Section Sorting 
    url(r'^section_sorting/$',
        SectionSortingView.as_view(),
        name='section_sorting'),

    # Indicator Sorting 
    url(r'^indicator_sorting/$',
        IndicatorSortingView.as_view(),
        name='indicator_sorting'),
]
