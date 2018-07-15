# -*- coding: utf-8 -*-


from django.views.generic import TemplateView
from .models import Slide
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from .forms import SlideForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.context_processors import PermWrapper
from reversion.views import RevisionMixin
from django.shortcuts import get_object_or_404
from reversion.models import Version
import reversion
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse


LETTERS = {
    u"E": u"Е",
    u"T": u"Т",
    u"O": u"О",
    u"P": u"Р",
    u"A": u"А",
    u"H": u"Н",
    u"K": u"К",
    u"X": u"Х",
    u"C": u"С",
    u"B": u"В",
    u"M": u"М",
    u"e": u"е",
    u"t": u"т",
    u"o": u"о",
    u"p": u"р",
    u"a": u"а",
    u"h": u"н",
    u"k": u"к",
    u"x": u"х",
    u"c": u"с",
    u"b": u"в",
    u"m": u"м",
}


# Slide List View
class SlideListView(TemplateView):
    template_name = "slider/slider_content.html"
    permission_required = ('slider.view_slide')

    def get_context_data(self, **kwargs):
        context = super(SlideListView, self).get_context_data(**kwargs)
        context['slides'] = Slide.objects.all()
        return context


# Slide Sorting View
class SlideSortingView(CsrfExemptMixin, JsonRequestResponseMixin, FormView):
    def post(self, request, *args, **kwargs):
        print self.request_json.items()
        for pk, idx in self.request_json.items():
            Slide.objects.filter(pk=pk).update(idx=idx)
        return self.render_json_response({'saved': 'ok'})


# Slide Create View
class SlideCreateView(PermissionRequiredMixin, RevisionMixin, CreateView):
    template_name = 'slider/create_slide.html'
    form_class = SlideForm
    permission_required = ('slider.add_slide')
    raise_exception = True

    def get(self, request, *args, **kwargs):
        data = dict()
        context = {'slide_create_form': SlideForm()}
        data['html_form'] = render_to_string('slider/create_slide.html', context, request=request)
        return JsonResponse(data)

    def form_valid(self, form):
        new_slide = form.save(commit=False)
        new_slide.head = u"".join(LETTERS.get(x, x) for x in form.cleaned_data['head'])
        new_slide.save()
        data = dict()
        data['form_is_valid'] = True
        context = {
            'slides': Slide.objects.all(),
            'perms': PermWrapper(self.request.user),
        }
        data['html_slides'] = render_to_string('slider/slides.html', context)
        reversion.set_comment('Создан')
        return JsonResponse(data)


# Slide Edit View
class SlideEditView(PermissionRequiredMixin, RevisionMixin, UpdateView):
    template_name = 'slider/edit_slide.html'
    form_class = SlideForm
    model = Slide
    permission_required = ('slider.change_slide')
    raise_exception = True

    def get(self, request, *args, **kwargs):
        data = dict()
        slide = Slide.objects.get(pk=self.kwargs['pk'])
        slide_edit_form = SlideForm(instance=slide)
        context = {'slide': slide, 'slide_edit_form': slide_edit_form}
        data['html_form'] = render_to_string('slider/edit_slide.html', context, request=request)
        return JsonResponse(data)

    def form_valid(self, form):
        new_slide = form.save(commit=False)
        new_slide.head = u"".join(LETTERS.get(x, x) for x in form.cleaned_data['head'])
        new_slide.save()
        data = dict()
        data['form_is_valid'] = True
        context = {
            'slides': Slide.objects.all(),
            'perms': PermWrapper(self.request.user),
        }
        data['html_slides'] = render_to_string('slider/slides.html', context)
        reversion.set_comment('Отредактирован')
        return JsonResponse(data)


# Slide Delete View
class SlideDeleteView(PermissionRequiredMixin, RevisionMixin, DeleteView):
    permission_required = ('slider.delete_slide')
    raise_exception = True

    def get(self, request, *args, **kwargs):
        slide = Slide.objects.get(pk=self.kwargs['pk'])
        data = dict()
        context = {'slide': slide}
        data['html_form'] = render_to_string('slider/delete_slide.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        slide = Slide.objects.get(pk=self.kwargs['pk'])
        slide.image.delete(save=True)
        slide.delete()
        data = dict()
        data['form_is_valid'] = True
        context = {
            'slides': Slide.objects.all(),
            'perms': PermWrapper(self.request.user),
        }
        data['html_slides'] = render_to_string('slider/slides.html', context)
        reversion.set_comment('Удален')
        return JsonResponse(data)


# Slide Reversions
class SlideReversions(DetailView):
    model = Slide
    template_name = 'slider/slide_reversions.html'

    def get_context_data(self, **kwargs):
        context = super(SlideReversions, self).get_context_data(**kwargs)
        slide = get_object_or_404(Slide, pk=self.kwargs.get('pk'))
        context['versions'] = Version.objects.get_for_object(slide)
        return context


# Slide Revert
class SlideRevert(PermissionRequiredMixin, RedirectView):
    permission_required = 'slider.revert_slide'

    @reversion.create_revision()
    def get_redirect_url(self, *args, **kwargs):
        slide=get_object_or_404(Slide, pk=self.kwargs.get('pk'))
        revision=get_object_or_404(Version.objects.get_for_object(slide), revision_id=self.kwargs.get('slide_reversion_id')).revision
        reversion.set_user(self.request.user)
        reversion.set_comment("Откат к версии #{}".format(revision.id))
        revision.revert()
        return reverse('slider:slide_reversions', args=(self.kwargs.get('pk'),))
