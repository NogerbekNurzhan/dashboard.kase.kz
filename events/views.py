# -*- coding: utf-8 -*-


from django.views.generic.base import RedirectView
from .models import Event
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import(
    DeleteView,
    CreateView,
    UpdateView,
    FormView
)
from django.contrib.auth.context_processors import PermWrapper
from django.template.loader import render_to_string
from django.http import JsonResponse
from .forms import (
    EventCreateForm,
    EventEditForm
)
import os
from CA.settings import EVENT_IMAGE_STORAGE
import uuid
import transliterate
from django.contrib.auth.mixins import PermissionRequiredMixin
from glob import glob
from django.views import View


# "Event" | Language
class EventLanguage(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse(
            'events:event_language_year',
            args=(
                self.kwargs.get('language'),
                Event.objects.filter(event_lang=self.kwargs.get('language')).dates('event_date', 'year').last().year
            )
        )


# Event List View: Year + Language
class EventLanguageYear(TemplateView):
    template_name = "events/event_content.html"
    permission_required = ('events.view_events')

    def get_context_data(self, **kwargs):
        context = super(EventLanguageYear, self).get_context_data(**kwargs)
        context['events'] = Event.objects.filter(event_lang=self.kwargs.get('language'), event_date__contains=self.kwargs.get('year'), event_removed=False)
        context['years'] = Event.objects.filter(event_lang=self.kwargs.get('language'), event_removed=False).dates('event_date', 'year')
        context['current_language'] =  self.kwargs.get('language')
        context['current_year'] = self.kwargs.get('year')
        context['languages'] = {'/ru/': 'Русский', '/en/': 'Английский', '/kz/': 'Казахский',}
        context['request_path'] = self.request.path
        context['use_wysiwyg_editor'] = self.request.user.user_permissions.filter(codename='use_wysiwyg_editor').exists()
        return context


# Event Delete
class EventDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'events/delete_event.html'
    permission_required = ('events.delete_event')
    raise_exception = True

    def get(self, request, *args, **kwargs):
        event = Event.objects.get(pk=self.kwargs['pk'])
        data = dict()
        context = {
            'event': event,
            'current_language': self.kwargs.get('language'),
            'current_year': self.kwargs.get('year'),
        }
        data['html_form'] = render_to_string('events/delete_event.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        # Текущее событие
        event = Event.objects.get(pk=self.kwargs['pk'])
        event.event_removed = True
        event.save()
        # Инициализируем pk события
        data = dict()
        data['event_id'] = event.pk
        # После скрытия события проверяем есть ли еще другие события
        if Event.objects.filter(event_lang=self.kwargs.get('language'), event_date__contains=self.kwargs.get('year'), event_removed=False).exists():
            data['event_exist'] = True
        else:
            data['event_exist'] = False
            # HTML событий
            data['html_events'] = render_to_string(
                'events/events.html',
                {
                    'events': Event.objects.filter(event_lang=self.kwargs.get('language'), event_date__contains=self.kwargs.get('year'), event_removed=False),
                    'perms': PermWrapper(self.request.user),
                    'current_language': self.kwargs.get('language'),
                    'current_year': self.kwargs.get('year'),
                }
            )
            # HTML списка годов
            data['html_years'] = render_to_string(
                'events/years.html',
                {
                    'years': Event.objects.filter(event_lang=self.kwargs.get('language'), event_removed=False).dates('event_date', 'year'),
                    'current_language': self.kwargs.get('language'),
                },
                request=self.request
            )
        data['form_is_valid'] = True
        return JsonResponse(data)


# Event Create
class EventCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'events/create_event.html'
    form_class = EventCreateForm
    permission_required = ('events.add_event')
    raise_exception = True

    def get(self, request, *args, **kwargs):
        data = dict()
        context = {
            'event_create_form': EventCreateForm(user=self.request.user),
            'current_language': self.kwargs.get('language'),
            'current_year': self.kwargs.get('year'),
            'use_wysiwyg_editor': self.request.user.user_permissions.filter(codename='use_wysiwyg_editor').exists(),
        }
        data['html_form'] = render_to_string('events/create_event.html', context, request=request)
        return JsonResponse(data)

    def form_valid(self, form):
        data = dict()
        # Перед созданием нового события проверяем наличия событий по заданным параметрам
        if Event.objects.filter(event_lang=self.kwargs.get('language'), event_date__contains=self.kwargs.get('year'), event_removed=False).exists():
            data['event_exist'] = True
        else:
            data['event_exist'] = False
        # Создаем новое событие
        new_event = form.save(commit=False)
        new_event.event_lang = self.kwargs.get('language')
        new_event.save()
        # Загрузить изображения в указанную директорию
        directory = EVENT_IMAGE_STORAGE + 'events/' + str(new_event.event_date.year) + '-' + new_event.event_shortname
        images = self.request.FILES.getlist('image_field')
        for image in images:
            if not os.path.exists(directory):
                os.makedirs(directory)
            filename, expansion = image.name.split('.')
            if transliterate.detect_language(filename)=='ru':
                if os.path.exists(directory + '/' + transliterate.translit(filename, reversed=True) + '.' + expansion):
                    with open(directory + '/' + transliterate.translit(filename, reversed=True) + str(uuid.uuid4().hex) + '.' + expansion, 'wb+') as destination:
                        for chunk in image.chunks():
                            destination.write(chunk)
                else:
                    with open(directory + '/' + transliterate.translit(filename, reversed=True) + '.' + expansion, 'wb+') as destination:
                        for chunk in image.chunks():
                            destination.write(chunk)
            else:
                if os.path.exists(directory + '/' + image.name):
                    with open(directory + '/' + filename + str(uuid.uuid4().hex) + '.' + expansion, 'wb+') as destination:
                        for chunk in image.chunks():
                            destination.write(chunk)
                else:
                    with open(directory + '/' + image.name, 'wb+') as destination:
                        for chunk in image.chunks():
                            destination.write(chunk)
        # Проверяем для какого года был создан новый документ
        if str(new_event.event_date.year)==str(self.kwargs.get('year')):
            data['equal_event_data'] = True
        else:
            data['equal_event_data'] = False
        # HTML нового события
        data['html_event'] = render_to_string(
            'events/event.html',
            {
                'event': new_event,
                'perms': PermWrapper(self.request.user),
                'current_language': self.kwargs.get('language'),
                'current_year': self.kwargs.get('year'),
            },
            request=self.request
        )
        # HTML событий
        data['html_events'] = render_to_string(
            'events/events.html',
            {
                'events': Event.objects.filter(event_lang=self.kwargs.get('language'), event_date__contains=self.kwargs.get('year'), event_removed=False),
                'perms': PermWrapper(self.request.user),
                'current_language': self.kwargs.get('language'),
                'current_year': self.kwargs.get('year'),
            }
        )
        # HTML списка годов
        data['html_years'] = render_to_string(
            'events/years.html',
            {
                'years': Event.objects.filter(event_lang=self.kwargs.get('language'), event_removed=False).dates('event_date', 'year'),
                'current_language': self.kwargs.get('language'),
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

    def get_form_kwargs(self):
        kwargs = super(EventCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


# Event Edit
class EventEditView(PermissionRequiredMixin, UpdateView):
    template_name = 'events/edit_event.html'
    form_class = EventEditForm
    model = Event
    permission_required = ('events.change_event')
    raise_exception = True

    def get(self, request, *args, **kwargs):
        data = dict()
        event = Event.objects.get(pk=self.kwargs['pk'])
        event_edit_form = EventEditForm(instance=event, user=self.request.user)
        path=EVENT_IMAGE_STORAGE+'events/'+self.kwargs.get('year')+"-"+event.event_shortname
        # Выгружаем список всех документов связанных с событием
        image_dictionaty = {}
        if os.path.exists(EVENT_IMAGE_STORAGE+'events/'+self.kwargs.get('year')+"-"+event.event_shortname):
            for file in os.listdir(path):
                if file.endswith(tuple((".png", ".PNG", ".jpg", ".JPG", ".gif", ".GIF"))):
                    if os.path.isfile(os.path.join(path, file)):
                        file_name = file
                        file = 'files/events/'+self.kwargs.get('year')+"-"+event.event_shortname+'/'+file
                        image_dictionaty.update({file_name: file})
        else:
            image_dictionaty = {}
        context = {
            'event': event,
            'current_language': self.kwargs.get('language'),
            'current_year': self.kwargs.get('year'),
            'event_edit_form': event_edit_form,
            'use_wysiwyg_editor': self.request.user.user_permissions.filter(codename='use_wysiwyg_editor').exists(),
            'images': image_dictionaty,
        }
        data['html_form'] = render_to_string('events/edit_event.html', context, request=request)
        return JsonResponse(data)

    def form_valid(self, form):
        edited_event = form.save(commit=False)
        edited_event.save()
        data = dict()
        data['event_id'] = edited_event.pk  # Инициализируем pk события
        # Загрузить изображения в указанную директорию
        directory = EVENT_IMAGE_STORAGE + 'events/' + str(edited_event.event_date.year) + '-' + edited_event.event_shortname
        images = self.request.FILES.getlist('image_field')
        for image in images:
            if not os.path.exists(directory):
                os.makedirs(directory)
            filename, expansion = image.name.split('.')
            if transliterate.detect_language(filename)=='ru':
                if os.path.exists(directory + '/' + transliterate.translit(filename, reversed=True) + '.' + expansion):
                    with open(directory + '/' + transliterate.translit(filename, reversed=True) + str(uuid.uuid4().hex) + '.' + expansion, 'wb+') as destination:
                        for chunk in image.chunks():
                            destination.write(chunk)
                else:
                    with open(directory + '/' + transliterate.translit(filename, reversed=True) + '.' + expansion, 'wb+') as destination:
                        for chunk in image.chunks():
                            destination.write(chunk)
            else:
                if os.path.exists(directory + '/' + image.name):
                    with open(directory + '/' + filename + str(uuid.uuid4().hex) + '.' + expansion, 'wb+') as destination:
                        for chunk in image.chunks():
                            destination.write(chunk)
                else:
                    with open(directory + '/' + image.name, 'wb+') as destination:
                        for chunk in image.chunks():
                            destination.write(chunk)
        # HTML редактируемого события
        data['html_event'] = render_to_string(
            'events/event.html',
            {
                'event': edited_event,
                'perms': PermWrapper(self.request.user),
                'current_language': self.kwargs.get('language'),
                'current_year': self.kwargs.get('year'),
            },
            request=self.request
        )
        data['form_is_valid'] = True
        return JsonResponse(data)

    def form_invalid(self, form):
        data = dict()
        data['form_is_valid'] = False
        data['form_errors'] = form.errors
        return JsonResponse(data)

    def get_form_kwargs(self):
        kwargs = super(EventEditView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


# Image Delete
class ImageDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('events.change_event')
    raise_exception = True

    def post(self, request, *args, **kwargs):
        # Инициализируем словарь data
        data = dict()
        # Текущее событие
        event = Event.objects.get(pk=self.kwargs['pk'])
        # Удаление выбранных пользователем файлы
        images_checkbox = self.request.POST.getlist('images')
        for image_checkbox in images_checkbox:
            image_path = EVENT_IMAGE_STORAGE + 'events/' + str(event.event_date.year) + "-" + event.event_shortname + "/" + image_checkbox
            if os.path.exists(image_path):
                os.remove(image_path)
        # Формируем список всех документов связанных с событием после операции удаления
        path=EVENT_IMAGE_STORAGE+'events/'+str(event.event_date.year)+"-"+event.event_shortname
        image_dictionaty = {}
        if os.path.exists(path):
            for file in os.listdir(path):
                if file.endswith(tuple((".png", ".PNG", ".jpg", ".JPG", ".gif", ".GIF"))):
                    if os.path.isfile(os.path.join(path, file)):
                        file_name = file
                        file = 'files/events/'+str(event.event_date.year)+"-"+event.event_shortname+'/'+file
                        image_dictionaty.update({file_name: file})
        else:
            image_dictionaty = {}
        # HTML блока с изображениями
        data['html_images'] = render_to_string(
            'events/images.html',
            {
                'images': image_dictionaty,
            },
        )
        data['form_is_valid'] = True
        return JsonResponse(data)
