# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from slider.models import Slide
from documents.models import Document
from static_pages.models import StaticPage


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['slides'] = Slide.objects.all()
        context['static_pages'] = StaticPage.objects.all()
        return context
