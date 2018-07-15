# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as authentication_views
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from CA.views import DashboardView
from CA.forms import AdministrationAuthenticationForm


urlpatterns = [
    # Dashboard Page (Home Page)
    url(r'^$',
        login_required(
            login_url=reverse_lazy('administration_login'))
        (DashboardView.as_view()),
        name='dashboard'),

    # Login
    url(r'^login/$',
        authentication_views.login,
        {
            'template_name': 'administration/login.html',
            'authentication_form': AdministrationAuthenticationForm,
            'extra_context': {
                'next': reverse_lazy('dashboard'),
            },
            'redirect_field_name': next,
            'redirect_authenticated_user': True
        },
        name='administration_login'),

    # Logout
    url(r'^logout/$',
        authentication_views.logout,
        {
            'next_page': reverse_lazy('dashboard')
        },
        name='administration_logout'),

    # "Slider" Module
    url(r'^slide/',
        include('slider.urls', namespace='slider')),

    # "Static Page" Module
    url(r'^static_page/',
        include('static_pages.urls', namespace='static_page')),

    # "User" Module
    url(r'^user/',
        include('users.urls', namespace='user')),

    # "Documents" application
    url(r'^documents/',
        include('documents.urls', namespace='documents')),

    # "Video" Module
    url(r'^video/',
        include('video.urls', namespace='video')),

    # 'Indicators' Module
    url(r'^sections_indicators/',
        include('indicators.urls', namespace='indicators')),

    # "Events" Module
    url(r'^events/',
        include('events.urls', namespace='events')),

    # "FAQ" Module
    url(r'^faq/',
        include('faq.urls', namespace='faq')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
