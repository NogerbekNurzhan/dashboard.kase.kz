# -*- coding: utf-8 -*-


from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from .views import StaticPageListView, StaticPageCreateView, StaticPageEditView, StaticPageDeleteView
from .views import StaticPageSortingView, StaticPageReversions, StaticPageRevert

urlpatterns = [
    # Static Page List
    url(r'^$',
        login_required(login_url=reverse_lazy('administration_login'))(StaticPageListView.as_view()),
        name='static_page_list'),

    # Static Page Create
    url(r'^create/$',
        StaticPageCreateView.as_view(),
        name='static_page_create'),

    # Static Page Delete
    url(r'^(?P<pk>\d+)/delete/$',
        StaticPageDeleteView.as_view(),
        name='static_page_delete'),

    # Static Page Edit
    url(r'^(?P<pk>\d+)/edit/$',
        StaticPageEditView.as_view(),
        name='static_page_edit'),

    # Sorting Static Page
    url(r'^sorting/$',
        StaticPageSortingView.as_view(),
        name='static_page_sorting'),

    # Static Page Revisions
    url(r'^(?P<pk>\d+)/reversions/$',
        StaticPageReversions.as_view(),
        name='static_page_reversions'),

    # Static Page Revert
    url(r'^(?P<pk>\d+)/reversions/(?P<static_page_reversion_id>\d+)/static_page_revert/$',
        StaticPageRevert.as_view(),
        name='static_page_revert'),
]
