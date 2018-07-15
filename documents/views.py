# -*- coding: utf-8 -*-


from django.views.generic.list import ListView
from django.views.generic import TemplateView
from .models import (
    Document,
    DocumentClosure
)
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views import View
from django.db import connection
from django.shortcuts import redirect
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse
from django.http import JsonResponse, HttpResponse
import json
from el_pagination.views import AjaxListView
from .forms import DocumentForm
from django.template.loader import render_to_string
from django.template import RequestContext
from urlparse import urlparse
from django.shortcuts import render
from braces.views import MultiplePermissionsRequiredMixin
from django.contrib.auth.context_processors import PermWrapper


# Category | Sidebar Menu
class DocumentCategory(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.kwargs.get('category')==str(8):
            return reverse('documents:category_tab', args=(self.kwargs.get('category'), 5))
        else:
            return reverse('documents:category_year', args=(self.kwargs.get('category'), Document.objects.filter(category=self.kwargs.get('category')).dates('date_add', 'year').last().year))


# ListView: Category + Year
class DocumentCategoryYear(AjaxListView):
    context_object_name = 'documents'
    template_name = "documents/document_content.html"
    page_template = 'documents/documents.html'

    def get_queryset(self):
        documents = Document.objects.filter(category=self.kwargs.get('category'), date_add__contains=self.kwargs.get('year'), parent__isnull=True, del_field=False)
        for document in documents:
            document.prepopulate(document.get_descendants())
        return documents

    def get_context_data(self, **kwargs):
        context = super(DocumentCategoryYear, self).get_context_data(**kwargs)
        context['current_category'] = self.kwargs.get('category')
        context['current_year'] = self.kwargs.get('year')
        context['years'] = Document.objects.filter(category=self.kwargs.get('category'), del_field=False).dates('date_add', 'year')
        context['request_path'] = self.request.path
        return context


# ListView: Category + Tab
class DocumentCategoryTab(AjaxListView):
    context_object_name = 'documents'
    template_name = "documents/document_content.html"
    page_template = 'documents/documents.html'

    def get_queryset(self):
        documents = Document.objects.filter(category=self.kwargs.get('category'), tab=self.kwargs.get('tab'), parent__isnull=True, del_field=False)
        for document in documents:
            document.prepopulate(document.get_descendants())
        return documents

    def get_context_data(self, **kwargs):
        context = super(DocumentCategoryTab, self).get_context_data(**kwargs)
        context['current_category'] = self.kwargs.get('category')
        context['current_tab'] = self.kwargs.get('tab')
        context['tabs'] = list(set(Document.objects.filter(category=self.kwargs.get('category'), del_field=False).values_list('tab', flat=True)))
        context['request_path'] = self.request.path
        return context


# Document Search
class DocumentSearch(AjaxListView):
    def post(self, request, *args, **kwargs):
        context = {
            'documents': Document.objects.filter(category=self.kwargs.get('category'), title__icontains=self.request.POST['search_text'], del_field=False),
            'current_category': self.kwargs.get('category'),
        }
        return render(request, 'documents/document_search_result.html', context)


# Function parse JSON which was send by Nestable2|AJAX and return list of ids
def get_ids(json_array):
    ids = []
    for obj in json_array:
        if isinstance(obj, dict):
            ids.append(obj.get('id'))
            children = obj.get('children')
            if children:
                ids.extend(get_ids(children))
        elif isinstance(obj, list):
            ids.extend(get_ids(obj))
    return ids


# Save new order of documents tree structure
class DocumentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, MultiplePermissionsRequiredMixin, FormView):
    permissions = {
        "any": (
            'documents.change_order_document_1',
            'documents.change_order_document_2',
            'documents.change_order_document_3',
            'documents.change_order_document_4',
            'documents.change_order_document_5',
            'documents.change_order_document_7',
            'documents.change_order_document_8',
            'documents.change_order_document_9',
            'documents.change_order_document_11',
            'documents.change_order_document_12',
        )
    }
    raise_exception = True

    def post(self, request, *args, **kwargs):
        # Update data in "document" table
        Document.document_table_update(None, self.request_json)
        # Delete data from "document closure" table
        DocumentClosure.objects.filter(parent_id__in=get_ids(self.request_json)).delete()
        # Create data in "document closure" table
        DocumentClosure.objects.bulk_create([DocumentClosure(
            parent_id=x['pk'],
            child_id=x['pk'],
            depth=0
        ) for x in Document.objects.filter(pk__in=get_ids(self.request_json)).values("pk")])
        for node in Document.objects.filter(pk__in=get_ids(self.request_json)):
            node._closure_createlink()
        return self.render_json_response({'saved': 'ok'})


# Document Create | Category + Year
class DocumentCategoryYearCreate(MultiplePermissionsRequiredMixin, CreateView):
    template_name = 'documents/create_document.html'
    form_class = DocumentForm
    permissions = {
        "any": (
            'documents.add_document_1',
            'documents.add_document_2',
            'documents.add_document_3',
            'documents.add_document_4',
            'documents.add_document_5',
            'documents.add_document_7',
            'documents.add_document_9',
            'documents.add_document_11',
            'documents.add_document_12',
        )
    }
    raise_exception = True

    def get(self, request, *args, **kwargs):
        data = dict()
        context = {
            'document_create_form': DocumentForm(),
            'current_category': self.kwargs.get('category'),
            'current_year': self.kwargs.get('year'),
        }
        data['html_form'] = render_to_string('documents/create_document.html', context, request=request)
        return JsonResponse(data)

    def form_valid(self, form):
        data = dict()

        # Перед созданием нового документа проверяем наличия документов по заданным параметрам
        if Document.objects.filter(category=self.kwargs.get('category'), date_add__contains=form.cleaned_data['date_add'].year, del_field=False).exists():
            data['documents_exist'] = True
        else:
            data['documents_exist'] = False

        # Проверяем для какого года был создан новый документ
        if str(form.cleaned_data['date_add'].year)==str(self.kwargs.get('year')):
            data['equal_data_add'] = True
        else:
            data['equal_data_add'] = False

        # Cоздание нового документа
        new_document = form.save(commit=False)
        new_document.category = self.kwargs.get('category')
        new_document.author_id = self.request.user.id
        if form.cleaned_data['src_url']:
            new_document.src = urlparse(form.cleaned_data['src_url']).path[1:]
        new_document.save()

        # HTML нового документа
        data['html_document'] = render_to_string(
            'documents/document.html',
            {
                'node': new_document,
                'perms': PermWrapper(self.request.user),
                'current_category': self.kwargs.get('category'),
                'current_year': new_document.date_add.year,
            },
            request=self.request
        )

        # HTML списка годов
        data['html_years'] = render_to_string(
            'documents/years.html',
            {
                'years': Document.objects.filter(category=self.kwargs.get('category'), del_field=False).dates('date_add', 'year'),
                'current_category': self.kwargs.get('category'),
            },
            request=self.request
        )

        # Валидная форма
        data['form_is_valid'] = True

        return JsonResponse(data)

    def form_invalid(self, form):
        data = dict()
        data['form_is_valid'] = False
        data['form_errors'] = form.errors
        return JsonResponse(data)


# Document Create | Category + Tab
class DocumentCategoryTabCreate(MultiplePermissionsRequiredMixin, CreateView):
    template_name = 'documents/create_document.html'
    form_class = DocumentForm
    permissions = {
        "any": (
            'documents.add_document_8',
        )
    }
    raise_exception = True

    def get(self, request, *args, **kwargs):
        data = dict()
        context = {
            'document_create_form': DocumentForm(),
            'current_category': self.kwargs.get('category'),
            'current_tab': self.kwargs.get('tab'),
        }
        data['html_form'] = render_to_string('documents/create_document.html', context, request=request)
        return JsonResponse(data)

    def form_valid(self, form):
        data = dict()

        # Перед созданием нового документа проверяем наличия документов по заданным пользовательским параметрам
        if Document.objects.filter(category=self.kwargs.get('category'), tab=form.cleaned_data['tab'], del_field=False).exists():
            data['documents_exist'] = True
        else:
            data['documents_exist'] = False

        # Проверяем для какой вкладки был создан новый документ
        if str(form.cleaned_data['tab'])==str(self.kwargs.get('tab')):
            data['equal_tab'] = True
        else:
            data['equal_tab'] = False

        # Cоздание нового документа
        new_document = form.save(commit=False)
        new_document.category = self.kwargs.get('category')
        new_document.author_id = self.request.user.id
        if form.cleaned_data['src_url']:
            new_document.src = urlparse(form.cleaned_data['src_url']).path[1:]
        new_document.save()

        # HTML нового документа
        data['html_document'] = render_to_string(
            'documents/document.html',
            {
                'node': new_document,
                'perms': PermWrapper(self.request.user),
                'current_category': self.kwargs.get('category'),
                'current_tab': new_document.tab,
            },
            request=self.request,
        )

        # HTML списка вкладок
        data['html_tabs'] = render_to_string(
            'documents/tabs.html',
            {
                'tabs': list(set(Document.objects.filter(category=self.kwargs.get('category'), del_field=False).values_list('tab', flat=True))),
                'current_category': self.kwargs.get('category'),
            },
            request=self.request,
        )

        # Валидная форма
        data['form_is_valid'] = True

        return JsonResponse(data)

    def form_invalid(self, form):
        data = dict()
        data['form_is_valid'] = False
        data['form_errors'] = form.errors
        return JsonResponse(data)


# Edit Document | Category + Year
class DocumentCategoryYearEdit(MultiplePermissionsRequiredMixin, UpdateView):
    template_name = 'documents/edit_document.html'
    form_class = DocumentForm
    model = Document
    permissions = {
        "any": (
            'documents.edit_document_1',
            'documents.edit_document_2',
            'documents.edit_document_3',
            'documents.edit_document_4',
            'documents.edit_document_5',
            'documents.edit_document_7',
            'documents.edit_document_9',
            'documents.edit_document_11',
            'documents.edit_document_12',
        )
    }
    raise_exception = True

    def get(self, request, *args, **kwargs):
        data = dict()
        document = Document.objects.get(pk=self.kwargs['pk'])
        document_edit_form = DocumentForm(instance=document)
        context = {
            'document': document,
            'document_edit_form': document_edit_form,
            'current_category': self.kwargs.get('category'),
            'current_year': self.kwargs.get('year'),
        }
        data['html_form'] = render_to_string('documents/edit_document.html', context, request=request)
        return JsonResponse(data)

    def form_valid(self, form):
        data = dict()

        # Текущий документ с которым работает пользователь
        document = Document.objects.get(pk=self.kwargs['pk'])

        # Начальный год документа
        start_year = document.date_add.year

        # ВНАЧАЛЕ: Перед сохранением новых данных документа проверяем наличия документов по заданным параметрам
        if Document.objects.filter(category=self.kwargs.get('category'), date_add__contains=form.cleaned_data['date_add'].year, del_field=False).exists():
            data['documents_exist_start'] = True
        else:
            data['documents_exist_start'] = False

        # Проверяем изменился ли год публикации у редактируемого документа
        if str(form.cleaned_data['date_add'].year)==str(document.date_add.year) and document.parent==None:
            data['equal_data_add'] = True
        else:
            data['equal_data_add'] = False
            document.get_descendants().update(date_add=form.cleaned_data['date_add'])

        # Сохраняем отредактированные данные документа
        if form.cleaned_data['src_url']:
            new_document = form.save(commit=False)
            new_document.src = urlparse(form.cleaned_data['src_url']).path[1:]
            new_document.save()
        else:
            form.save()

        # ID документа с котором работает пользователь
        data['document_id'] = self.kwargs['pk']

        # HTML отредактированного документа
        data['html_document'] = render_to_string(
            'documents/document.html',
            {
                'node': Document.objects.get(pk=self.kwargs['pk']),
                'perms': PermWrapper(self.request.user),
                'current_category': self.kwargs.get('category'),
                'current_year': self.kwargs.get('year'),
            },
            request=self.request
        )

        # ВКОНЦЕ: После сохранения новых данных документа проверяем наличия документов по заданным параметрам
        if Document.objects.filter(category=self.kwargs.get('category'), date_add__contains=start_year, del_field=False).exists():
            data['documents_exist_end'] = True
        else:
            data['documents_exist_end'] = False

        # HTML списка годов
        data['html_years'] = render_to_string(
            'documents/years.html',
            {
                'years': Document.objects.filter(category=self.kwargs.get('category'), del_field=False).dates('date_add', 'year'),
                'current_category': self.kwargs.get('category'),
            },
            request=self.request
        )

        # Валидная форма
        data['form_is_valid'] = True

        return JsonResponse(data)

    def form_invalid(self, form):
        data = dict()
        data['form_is_valid'] = False
        data['form_errors'] = form.errors
        print(form.errors)
        return JsonResponse(data)


# Edit Document | Category + Tab
class DocumentCategoryTabEdit(MultiplePermissionsRequiredMixin, UpdateView):
    template_name = 'documents/edit_document.html'
    form_class = DocumentForm
    model = Document
    permissions = {
        "any": (
            'documents.edit_document_8',
        )
    }
    raise_exception = True

    def get(self, request, *args, **kwargs):
        data = dict()
        document = Document.objects.get(pk=self.kwargs['pk'])
        document_edit_form = DocumentForm(instance=document)
        context = {
            'document': document,
            'document_edit_form': document_edit_form,
            'current_category': self.kwargs.get('category'),
            'current_tab': self.kwargs.get('tab'),
        }
        data['html_form'] = render_to_string('documents/edit_document.html', context, request=request)
        return JsonResponse(data)

    def form_valid(self, form):
        data = dict()

        # Текущий документ с которым работает пользователь
        document = Document.objects.get(pk=self.kwargs['pk'])

        # Начальная вкладка документа
        start_tab = document.tab

        # Перед сохранением новых данных документа проверяем наличия документов по заданным параметрам
        if Document.objects.filter(category=self.kwargs.get('category'), tab=form.cleaned_data['tab'], del_field=False).exists():
            data['documents_exist_start'] = True
        else:
            data['documents_exist_start'] = False

        # Проверяем изменился ли год публикации у редактируемого документа
        if str(form.cleaned_data['tab'])==str(document.tab) and document.parent==None:
            data['equal_tab'] = True
        else:
            data['equal_tab'] = False
            document.get_descendants().update(tab=form.cleaned_data['tab'])

        # Сохраняем отредактированные данные документа
        if form.cleaned_data['src_url']:
            new_document = form.save(commit=False)
            new_document.src = urlparse(form.cleaned_data['src_url']).path[1:]
            new_document.save()
        else:
            form.save()

        # ID документа с котором работает пользователь
        data['document_id'] = self.kwargs['pk']

        # HTML отредактированного документа
        data['html_document'] = render_to_string(
            'documents/document.html',
            {
                'node': Document.objects.get(pk=self.kwargs['pk']),
                'perms': PermWrapper(self.request.user),
                'current_category': self.kwargs.get('category'),
                'current_tab': self.kwargs.get('tab'),
            },
            request=self.request
        )

        # ВКОНЦЕ: После сохранения новых данных документа проверяем наличия документов по заданным параметрам
        if Document.objects.filter(category=self.kwargs.get('category'), tab=start_tab, del_field=False).exists():
            data['documents_exist_end'] = True
        else:
            data['documents_exist_end'] = False

        # HTML списка вкладок
        data['html_tabs'] = render_to_string(
            'documents/tabs.html',
            {
                'tabs': list(set(Document.objects.filter(category=self.kwargs.get('category'), del_field=False).values_list('tab', flat=True))),
                'current_category': self.kwargs.get('category'),
            },
            request=self.request,
        )

        # Валидная форма
        data['form_is_valid'] = True

        return JsonResponse(data)

    def form_invalid(self, form):
        data = dict()
        data['form_is_valid'] = False
        data['form_errors'] = form.errors
        return JsonResponse(data)


# Document Delete | Category + Year
class DocumentCategoryYearDelete(MultiplePermissionsRequiredMixin, DeleteView):
    permissions = {
        "any": (
            'documents.delete_document_1',
            'documents.delete_document_2',
            'documents.delete_document_3',
            'documents.delete_document_4',
            'documents.delete_document_5',
            'documents.delete_document_7',
            'documents.delete_document_9',
            'documents.delete_document_11',
            'documents.delete_document_12',
        )
    }
    raise_exception = True

    def get(self, request, *args, **kwargs):
        document = Document.objects.get(pk=self.kwargs['pk'])
        data = dict()
        context = {
            'document': document,
            'current_category': self.kwargs.get('category'),
            'current_year': self.kwargs.get('year'),
        }
        data['html_form'] = render_to_string('documents/delete_document.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = dict()

        # ID выбранного пользователем документа
        data['document_id'] = self.kwargs['pk']

        # Удаляем выбранный пользователем документ
        document = Document.objects.get(pk=self.kwargs['pk'])
        document.get_descendants().delete()
        document.src.delete(save=True)
        document.delete()

        # Проверяем есть ли в списке еще документы
        if Document.objects.filter(category=self.kwargs.get('category'), date_add__contains=self.kwargs.get('year'), del_field=False).exists():
            data['documents_exist'] = True
        else:
            data['documents_exist'] = False

        # Валидная форма
        data['form_is_valid'] = True

        return JsonResponse(data)

    def form_invalid(self, form):
        data = dict()
        data['form_is_valid'] = False
        data['form_errors'] = form.errors
        return JsonResponse(data)


# Document Delete | Category + Tab
class DocumentCategoryTabDelete(MultiplePermissionsRequiredMixin, DeleteView):
    permissions = {
        "any": (
            'documents.delete_document_8',
        )
    }
    raise_exception = True

    def get(self, request, *args, **kwargs):
        document = Document.objects.get(pk=self.kwargs['pk'])
        data = dict()
        context = {
            'document': document,
            'current_category': self.kwargs.get('category'),
            'current_tab': self.kwargs.get('tab'),
        }
        data['html_form'] = render_to_string('documents/delete_document.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = dict()

        # ID выбранного пользователем документа
        data['document_id'] = self.kwargs['pk']

        # Удаляем выбранный пользователем документ
        document = Document.objects.get(pk=self.kwargs['pk'])
        document.get_descendants().delete()
        document.src.delete(save=True)
        document.delete()

        # Проверяем есть ли в списке еще документы
        if Document.objects.filter(category=self.kwargs.get('category'), tab=self.kwargs.get('tab'), del_field=False).exists():
            data['documents_exist'] = True
        else:
            data['documents_exist'] = False

        # Валидная форма
        data['form_is_valid'] = True

        return JsonResponse(data)

    def form_invalid(self, form):
        data = dict()
        data['form_is_valid'] = False
        data['form_errors'] = form.errors
        return JsonResponse(data)
