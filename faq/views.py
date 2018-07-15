# -*- coding: utf-8 -*-


from django.views.generic import TemplateView
from .models import FAQ
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.views.generic.edit import(
	FormView,
	CreateView,
	UpdateView,
	DeleteView,
)
from .forms import FAQForm
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.context_processors import PermWrapper


# "FAQ" | Language
class FAQLanguage(TemplateView):
    template_name = "faq/faq_content.html"

    def get_context_data(self, **kwargs):
        context = super(FAQLanguage, self).get_context_data(**kwargs)
        context['questions'] = FAQ.objects.filter(lang=self.kwargs.get('language'))
        context['current_language'] =  self.kwargs.get('language')
        context['languages'] = {'/ru/': 'Русский', '/en/': 'Английский', '/kz/': 'Казахский',}
        return context

# FAQ Sorting View
class FAQSortingView(CsrfExemptMixin, JsonRequestResponseMixin, FormView):
    def post(self, request, *args, **kwargs):
        print self.request_json.items()
        for pk, position in self.request_json.items():
            FAQ.objects.filter(pk=pk).update(position=position)
        return self.render_json_response({'saved': 'ok'})


# FAQ Delete
class FAQDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'faq/delete_faq.html'
    permission_required = ('faq.delete_faq')
    raise_exception = True

    def get(self, request, *args, **kwargs):
        question = FAQ.objects.get(pk=self.kwargs['pk'])
        data = dict()
        context = {
            'question': question,
            'current_language': self.kwargs.get('language'),
            'perms': PermWrapper(self.request.user),
        }
        data['html_form'] = render_to_string('faq/delete_faq.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        # Находим текущий вопрос
        question = FAQ.objects.get(pk=self.kwargs['pk'])
        # Инициализируем pk события
        data = dict()
        data['question_id'] = question.pk
        # Удаляем вопрос из базы данных
        question.delete()
        # После скрытия/удаления вопроса проверяем есть ли еще другие вопросы
        queryset = FAQ.objects.filter(lang=self.kwargs.get('language'))
        if queryset:
            data['question_exist'] = True
        else:
            data['question_exist'] = False
            # HTML вопросов в случаи если вопросов больше нету
            data['html_questions'] = render_to_string(
                'faq/questions.html',
                {
                    'questions': queryset,
                    'current_language': self.kwargs.get('language'),
                    'perms': PermWrapper(self.request.user),
                }
            )
        data['form_is_valid'] = True
        return JsonResponse(data)


# FAQ Create
class FAQCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'faq/create_faq.html'
    form_class = FAQForm
    permission_required = ('faq.add_faq')
    raise_exception = True

    def get(self, request, *args, **kwargs):
        data = dict()
        context = {
            'faq_create_form': FAQForm(),
            'current_language': self.kwargs.get('language'),
        }
        data['html_form'] = render_to_string('faq/create_faq.html', context, request=request)
        return JsonResponse(data)

    def form_valid(self, form):
        data = dict()
        # Создаем новый вопрос
        new_question = form.save(commit=False)
        new_question.lang = self.kwargs.get('language')
        new_question.save()
        # После создания нового вопроса проверяем наличия вопросов по заданным параметрам
        if FAQ.objects.filter(lang=self.kwargs.get('language')).count()==1:
            data['question_exist'] = True
            # HTML вопросов
            data['html_questions'] = render_to_string(
                'faq/questions.html',
                {
                    'questions': FAQ.objects.filter(event_lang=self.kwargs.get('language')),
                    'current_language': self.kwargs.get('language'),
                    'perms': PermWrapper(self.request.user),
                }
            )
        else:
            data['question_exist'] = False
            # HTML нового вопроса
            data['html_question'] = render_to_string(
                'faq/question.html',
                {
                    'question': new_question,
                    'current_language': self.kwargs.get('language'),
                    'perms': PermWrapper(self.request.user),
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


# FAQ Edit
class FAQEditView(PermissionRequiredMixin, UpdateView):
    template_name = 'faq/edit_faq.html'
    form_class = FAQForm
    model = FAQ
    permission_required = ('faq.change_faq')
    raise_exception = True

    def get(self, request, *args, **kwargs):
        data = dict()
        question = FAQ.objects.get(pk=self.kwargs['pk'])
        faq_edit_form = FAQForm(instance=question)
        context = {
            'faq_edit_form': faq_edit_form,
            'current_language': self.kwargs.get('language'),
            'question': question,
        }
        data['html_form'] = render_to_string('faq/edit_faq.html', context, request=request)
        return JsonResponse(data)

    def form_valid(self, form):
        question = form.save(commit=False)
        question.save()
        data = dict()
        data['question_id'] = question.pk  # Инициализируем pk вопроса
        # HTML редактируемого вопроса
        data['html_question'] = render_to_string(
            'faq/question.html',
            {
                'question': question,
                'current_language': self.kwargs.get('language'),
                'perms': PermWrapper(self.request.user),
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
