# -*- coding: utf-8 -*-


from django.views.generic import TemplateView
from .models import FiniSection, FiniCode
from collections import OrderedDict
from .forms import FiniSectionForm, FiniCodeForm
from django.views.generic.edit import FormView, UpdateView
from django.template.loader import render_to_string
from django.http import JsonResponse
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
import re
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.context_processors import PermWrapper


# Section List View
class SectionListView(TemplateView):
    template_name = "indicators/indicator_content.html"
    permission_required = ('indicators.view_indicators')

    def get_context_data(self, **kwargs):
        context = super(SectionListView, self).get_context_data(**kwargs)
        sections = FiniSection.objects.all().prefetch_related('finicode_set').order_by('orderby')
        dictionary = OrderedDict()
        for section in sections:
            dictionary[section] = section.finicode_set.all()
        context['dictionary'] = dictionary
        context['indicators_without_section'] = FiniCode.objects.filter(section__isnull=True).order_by('fini_code_so')
        return context


# Section Edit View
class SectionEditView(PermissionRequiredMixin, UpdateView):
    template_name = 'indicators/edit_section.html'
    form_class = FiniSectionForm
    model = FiniSection
    permission_required = ('indicators.edit_section_of_indicators')
    raise_exception = True

    def get(self, request, *args, **kwargs):
        data = dict()
        section = FiniSection.objects.get(pk=self.kwargs['pk'])
        section_edit_form = FiniSectionForm(instance=section)
        context = {'section': section, 'section_edit_form': section_edit_form}
        data['html_form'] = render_to_string('indicators/edit_section.html', context, request=request)
        return JsonResponse(data)

    def form_valid(self, form):
        form.save()
        section = FiniSection.objects.get(pk=self.kwargs['pk']) 
        data = dict()
        data['section_id'] = section.id
        data['html_section_header'] = render_to_string(
            'indicators/section_header.html',
            {
                'section': section,
                'perms': PermWrapper(self.request.user),
            }
        )
        data['form_is_valid'] = True
        return JsonResponse(data)

    def form_invalid(self, form):
        data = dict()
        data['form_is_valid'] = False
        data['form_errors'] = form.errors
        return JsonResponse(data)


# Indicator Edit View
class IndicatorEditView(PermissionRequiredMixin, UpdateView):
    template_name = 'indicators/edit_indicator.html'
    form_class = FiniCodeForm
    model = FiniCode
    permission_required = ('indicators.edit_indicator')
    raise_exception = True

    def get(self, request, *args, **kwargs):
        data = dict()
        indicator = FiniCode.objects.get(pk=self.kwargs['pk'])
        indicator_edit_form = FiniCodeForm(instance=indicator)
        context = {'indicator': indicator, 'indicator_edit_form': indicator_edit_form}
        data['html_form'] = render_to_string('indicators/edit_indicator.html', context, request=request)
        return JsonResponse(data)

    def form_valid(self, form):
        form.save()
        indicator = FiniCode.objects.get(pk=self.kwargs['pk'])
        data = dict()
        data['indicator_id'] = indicator.id
        data['html_indicator'] = render_to_string(
            'indicators/indicator.html',
            {
                'indicator': indicator,
                'perms': PermWrapper(self.request.user),
            }
        )
        data['form_is_valid'] = True
        return JsonResponse(data)

    def form_invalid(self, form):
        data = dict()
        data['form_is_valid'] = False
        data['form_errors'] = form.errors
        print(form.errors)
        return JsonResponse(data)


# Section Sorting View
class SectionSortingView(CsrfExemptMixin, JsonRequestResponseMixin, FormView):
    def post(self, request, *args, **kwargs):
        for pk, orderby in self.request_json.items():
            FiniSection.objects.filter(pk=pk).update(orderby=orderby)
        return self.render_json_response({'saved': 'ok'})


# Indicator Sorting View
class IndicatorSortingView(CsrfExemptMixin, JsonRequestResponseMixin, FormView):
    def post(self, request, *args, **kwargs):
        for key, value in self.request_json.items():
            section_id = int(re.findall(r'^\D*(\d+)', key)[0])
            idx = 1
            for item in value:
                if section_id==0:
                    FiniCode.objects.filter(pk=int(re.findall(r'^\D*(\d+)', item)[0])).update(section=None, fini_code_so=idx)
                else:
                    FiniCode.objects.filter(pk=int(re.findall(r'^\D*(\d+)', item)[0])).update(section=section_id, fini_code_so=idx)
                idx += 1
        return self.render_json_response({'saved': 'ok'})

