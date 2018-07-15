# -*- coding: utf-8 -*-


from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from .views import SlideListView, SlideCreateView, SlideDeleteView, SlideEditView
from .views import SlideSortingView, SlideReversions, SlideRevert


urlpatterns = [
    # Slide List
    url(r'^$',
        login_required(login_url=reverse_lazy('administration_login'))(SlideListView.as_view()),
        name='slide_list'),

    # Slide Create
    url(r'^create/$',
        SlideCreateView.as_view(),
        name='slide_create'),

    # Slide Delete
    url(r'^(?P<pk>\d+)/delete/$',
        SlideDeleteView.as_view(),
        name='slide_delete'),

    # Slide Edit
    url(r'^(?P<pk>\d+)/edit/$',
        SlideEditView.as_view(),
        name='slide_edit'),

    # Slide Sorting 
    url(r'^sorting/$',
        SlideSortingView.as_view(),
        name='slide_sorting'),

    # Slide Revisions
    url(r'^(?P<pk>\d+)/reversions/$',
        SlideReversions.as_view(),
        name='slide_reversions'),

    # Slide Revert
    url(r'^(?P<pk>\d+)/reversions/(?P<slide_reversion_id>\d+)/slide_revert/$',
        SlideRevert.as_view(),
        name='slide_revert'),
]
