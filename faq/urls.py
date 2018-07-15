# -*- coding: utf-8 -*-


from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from .views import (
    FAQLanguage,
    FAQCreateView,
    FAQDeleteView,
    FAQEditView,
    FAQDeleteView,
    FAQSortingView
)


urlpatterns = [
    # "FAQ" | Language
    url(r'^(?P<language>[a-z]{2})/$',
        FAQLanguage.as_view(),
        name='faq_language'),

    # FAQ Create
    url(r'^(?P<language>[a-z]{2})/create/$',
        FAQCreateView.as_view(),
        name='faq_create'),

    # FAQ Delete
    url(r'^(?P<language>[a-z]{2})/(?P<pk>\d+)/delete/$',
        FAQDeleteView.as_view(),
        name='faq_delete'),

    # FAQ Edit
    url(r'^(?P<language>[a-z]{2})/(?P<pk>\d+)/edit/$',
        FAQEditView.as_view(),
        name='faq_edit'),

    # FAQ Sorting 
    url(r'^sorting/$',
        FAQSortingView.as_view(),
        name='faq_sorting'),
]
