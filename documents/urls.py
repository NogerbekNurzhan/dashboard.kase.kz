# -*- coding: utf-8 -*-


from django.conf.urls import url
from .views import (
    DocumentCategory,
    DocumentCategoryYear,
    DocumentCategoryTab,
    DocumentSearch,
    DocumentOrderView,
    DocumentCategoryYearCreate,
    DocumentCategoryTabCreate,
    DocumentCategoryYearEdit,
    DocumentCategoryTabEdit,
    DocumentCategoryYearDelete,
    DocumentCategoryTabDelete
)


urlpatterns = [
    # Category | Sidebar Menu
    url(r'^(?P<category>\d+)/$',
        DocumentCategory.as_view(),
        name='category'),

    # ListView: Category + Year
    url(r'^(?P<category>\d+)/(?P<year>[0-9]{4})/$',
        DocumentCategoryYear.as_view(),
        name='category_year'),

    # ListView: Category + Tab
    url(r'^(?P<category>\d+)/(?P<tab>\d+)/$',
        DocumentCategoryTab.as_view(),
        name='category_tab'),

    # Document Search by Category + Year
    url(r'^search/(?P<category>\d+)/$',
        DocumentSearch.as_view(),
        name='document_search'),

    # Document Order View
    url(r'^order/$',
        DocumentOrderView.as_view(),
        name='document_order'),

    # Create Document | Category + Year
    url(r'^(?P<category>\d+)/(?P<year>[0-9]{4})/create/$',
        DocumentCategoryYearCreate.as_view(),
        name='category_year_create'),

    # Create Document | Category + Tab
    url(r'^(?P<category>\d+)/(?P<tab>\d+)/create/$',
        DocumentCategoryTabCreate.as_view(),
        name='category_tab_create'),

    # Edit Document | Category Year
    url(r'^(?P<category>\d+)/(?P<year>[0-9]{4})/edit/(?P<pk>\d+)/$',
        DocumentCategoryYearEdit.as_view(),
        name='category_year_edit'),

    # Edit Document | Category Tab
    url(r'^(?P<category>\d+)/(?P<tab>\d+)/edit/(?P<pk>\d+)/$',
        DocumentCategoryTabEdit.as_view(),
        name='category_tab_edit'),

    # Delete Document | Category Year
    url(r'^(?P<category>\d+)/(?P<year>[0-9]{4})/delete/(?P<pk>\d+)/$',
        DocumentCategoryYearDelete.as_view(),
        name='category_year_delete'),

    # Delete Document | Category Tab
    url(r'^(?P<category>\d+)/(?P<tab>\d+)/delete/(?P<pk>\d+)/$',
        DocumentCategoryTabDelete.as_view(),
        name='category_tab_delete'),
]
