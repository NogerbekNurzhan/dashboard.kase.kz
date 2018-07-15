# -*- coding: utf-8 -*-


from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from .views import (
    VideoListView,
    VideoCreateView,
    VideoDeleteView,
    VideoEditView,
    VideoSortingView
)


urlpatterns = [
    # Video List
    url(r'^$',
        login_required(login_url=reverse_lazy('administration_login'))(VideoListView.as_view()),
        name='video_list'),

    # Video Create
    url(r'^create/$',
        VideoCreateView.as_view(),
        name='video_create'),

    # Video Delete
    url(r'^(?P<pk>\d+)/delete/$',
        VideoDeleteView.as_view(),
        name='video_delete'),

    # Video Edit
    url(r'^(?P<pk>\d+)/edit/$',
        VideoEditView.as_view(),
        name='video_edit'),

    # Video Sorting 
    url(r'^sorting/$',
        VideoSortingView.as_view(),
        name='video_sorting'),
]
