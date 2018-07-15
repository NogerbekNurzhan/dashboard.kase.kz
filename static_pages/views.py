# -*- coding: utf-8 -*-


from django.views.generic import TemplateView
from .models import StaticPage
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from .forms import StaticPageForm
from django.template.loader import render_to_string
from django.http import JsonResponse
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


# Static Page List View
class StaticPageListView(TemplateView):
    template_name = "static_pages/static_page_content.html"
    permission_required = ('static_pages.view_staticpage')

    def get_context_data(self, **kwargs):
        context = super(StaticPageListView, self).get_context_data(**kwargs)
        context['static_pages'] = StaticPage.objects.all()
        context['use_wysiwyg_editor'] = self.request.user.user_permissions.filter(codename='use_wysiwyg_editor').exists()
        return context


# Static Page Sorting View
class StaticPageSortingView(CsrfExemptMixin, JsonRequestResponseMixin, FormView):
    def post(self, request, *args, **kwargs):
        for pk, idx in self.request_json.items():
            StaticPage.objects.filter(pk=pk).update(idx=idx)
        return self.render_json_response({'saved': 'ok'})


# Static Page Create View
class StaticPageCreateView(PermissionRequiredMixin, RevisionMixin, CreateView):
    template_name = 'static_pages/create_static_page.html'
    form_class = StaticPageForm
    permission_required = ('static_pages.add_staticpage')
    raise_exception = True

    def get(self, request, *args, **kwargs):
        data = dict()
        context = {
            'static_page_create_form': StaticPageForm(user=self.request.user),
            'use_wysiwyg_editor': self.request.user.user_permissions.filter(codename='use_wysiwyg_editor').exists(),
        }
        data['html_form'] = render_to_string('static_pages/create_static_page.html', context, request=request)
        return JsonResponse(data)

    def form_valid(self, form):
        new_static_page = form.save(commit=False)
        new_static_page.head = u"".join(LETTERS.get(x, x) for x in form.cleaned_data['head'])
        new_static_page.save()
        print(form.errors.as_data())
        data = dict()
        data['form_is_valid'] = True
        context = {
            'static_pages': StaticPage.objects.all(),
            'perms': PermWrapper(self.request.user),
        }
        data['html_static_pages'] = render_to_string('static_pages/static_pages.html', context)
        reversion.set_comment('Создан')
        return JsonResponse(data)

    def get_form_kwargs(self):
        kwargs = super(StaticPageCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


# Edit Static Page
class StaticPageEditView(PermissionRequiredMixin, RevisionMixin, UpdateView):
    template_name = 'static_pages/edit_static_page.html'
    form_class = StaticPageForm
    model = StaticPage
    permission_required = ('static_pages.change_staticpage')
    raise_exception = True

    def get(self, request, *args, **kwargs):
        data = dict()
        static_page = StaticPage.objects.get(pk=self.kwargs['pk'])
        static_page_edit_form = StaticPageForm(instance=static_page, user=self.request.user)
        context = {
            'static_page': static_page,
            'static_page_edit_form': static_page_edit_form,
            'use_wysiwyg_editor': self.request.user.user_permissions.filter(codename='use_wysiwyg_editor').exists(),
        }
        data['html_form'] = render_to_string('static_pages/edit_static_page.html', context, request=request)
        return JsonResponse(data)

    def form_valid(self, form):
        new_static_page = form.save(commit=False)
        new_static_page.head = u"".join(LETTERS.get(x, x) for x in form.cleaned_data['head'])
        new_static_page.save()
        data = dict()
        data['form_is_valid'] = True
        context = {
            'static_pages': StaticPage.objects.all(),
            'perms': PermWrapper(self.request.user),
        }
        data['html_static_pages'] = render_to_string('static_pages/static_pages.html', context)
        reversion.set_comment('Отредактирован')
        return JsonResponse(data)

    def get_form_kwargs(self):
        kwargs = super(StaticPageEditView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


# Delete Static Page
class StaticPageDeleteView(PermissionRequiredMixin, RevisionMixin, DeleteView):
    permission_required = ('static_pages.delete_staticpage')
    raise_exception = True
    
    def get(self, request, *args, **kwargs):
        static_page = StaticPage.objects.get(pk=self.kwargs['pk'])
        data = dict()
        context = {'static_page': static_page}
        data['html_form'] = render_to_string('static_pages/delete_static_page.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        static_page = StaticPage.objects.get(pk=self.kwargs['pk'])
        static_page.delete()
        data = dict()
        data['form_is_valid'] = True
        context = {
            'static_pages': StaticPage.objects.all(),
            'perms': PermWrapper(self.request.user),
        }
        data['html_static_pages'] = render_to_string('static_pages/static_pages.html', context)
        reversion.set_comment('Удален')
        return JsonResponse(data)


# Static Page Reversions
class StaticPageReversions(DetailView):
    model = StaticPage
    template_name = 'static_pages/static_page_reversions.html'

    def get_context_data(self, **kwargs):
        context = super(StaticPageReversions, self).get_context_data(**kwargs)
        static_page = get_object_or_404(StaticPage, pk=self.kwargs.get('pk'))
        context['versions'] = Version.objects.get_for_object(static_page)
        return context


# Static Page Revert
class StaticPageRevert(PermissionRequiredMixin, RedirectView):
    permission_required = 'static_pages.revert_staticpage'

    @reversion.create_revision()
    def get_redirect_url(self, *args, **kwargs):
        static_page = get_object_or_404(StaticPage, pk=self.kwargs.get('pk'))
        revision = get_object_or_404(Version.objects.get_for_object(static_page), revision_id=self.kwargs.get('static_page_reversion_id')).revision
        reversion.set_user(self.request.user)
        reversion.set_comment("Откат к версии #{}".format(revision.id))
        revision.revert()
        return reverse('static_page:static_page_reversions', args=(self.kwargs.get('pk'),))
