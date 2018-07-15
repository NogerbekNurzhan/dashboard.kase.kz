# -*- coding: utf-8 -*-


from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from .forms import UserCreateForm, UserEditForm, UserPasswordChangeForm
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.models import Permission
from django.contrib.auth.context_processors import PermWrapper
from django.contrib.auth.mixins import PermissionRequiredMixin


# User List View
class UserListView(TemplateView):
    template_name = "users/user_content.html"

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['users'] = User.objects.order_by('username')
        return context


# User Create View
class UserCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'users/create_user.html'
    form_class = UserCreateForm
    model = User
    permission_required = 'auth.add_user'
    raise_exception = True

    def get(self, request, *args, **kwargs):
        data = dict()
        context = {'user_create_form': UserCreateForm()}
        data['html_form'] = render_to_string('users/create_user.html', context, request=request)
        return JsonResponse(data)

    def form_valid(self, form):
        form.save()
        data = dict()
        data['form_is_valid'] = True
        context = {
            'users': User.objects.order_by('username'),
            'perms': PermWrapper(self.request.user),
        }
        data['html_users'] = render_to_string('users/users.html', context)
        return JsonResponse(data)

    def form_invalid(self, form):
        data = dict()
        data['form_is_valid'] = False
        data['form_errors'] = form.errors
        return JsonResponse(data)


# User Edit View
class UserEditView(PermissionRequiredMixin, UpdateView):
    template_name = 'users/edit_user.html'
    form_class = UserEditForm
    model = User
    permission_required = 'auth.change_user'
    raise_exception = True
 
    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs['pk'])
        if user.is_superuser:
            user_role = 0
        elif user.is_staff:
            user_role = 1
        elif not user.is_superuser and not user.is_staff:
            user_role = 2
        if user.user_permissions.filter(codename='use_wysiwyg_editor').exists():
            use_wysiwyg_editor = True
        else:
            use_wysiwyg_editor = False
        context = {
            'user': user,
            'user_edit_form': UserEditForm(
                instance=user,
                initial={
                    'user_role': user_role,
                    'use_wysiwyg_editor': use_wysiwyg_editor
                }
            ),
        }
        data = dict()
        data['html_form'] = render_to_string('users/edit_user.html', context, request=request)
        return JsonResponse(data)

    def form_valid(self, form):
        user = form.save(commit=False)
        selected_user_role = form.cleaned_data['user_role']
        selected_use_wysiwyg_editor = form.cleaned_data['use_wysiwyg_editor']
        if "0" in selected_user_role:
            user.is_superuser = True
            for permission in Permission.objects.exclude(codename='use_wysiwyg_editor'):
                user.user_permissions.add(permission)
        elif "1" in selected_user_role:
            user.is_staff = True
            form.save_m2m()
        elif "2" in selected_user_role:
            user.is_superuser = False
            user.is_staff = False
            for permission in Permission.objects.exclude(codename='use_wysiwyg_editor'):
                user.user_permissions.remove(permission)

        if selected_use_wysiwyg_editor:
            user.user_permissions.add(Permission.objects.get(codename='use_wysiwyg_editor'))
        elif not selected_use_wysiwyg_editor:
            user.user_permissions.remove(Permission.objects.get(codename='use_wysiwyg_editor'))
        user.save()
        data = dict()
        data['form_is_valid'] = True
        context = {
            'users': User.objects.order_by('username'),
            'perms': PermWrapper(self.request.user),
        }
        data['html_users'] = render_to_string('users/users.html', context)
        return JsonResponse(data)

    def form_invalid(self, form):
        data = dict()
        data['form_is_valid'] = False
        data['form_errors'] = form.errors
        return JsonResponse(data)


# User Delete View
class UserDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'auth.delete_user'
    raise_exception = True

    def get(self, request, *args, **kwargs):
        data = dict()
        context = {'user': User.objects.get(pk=self.kwargs['pk']),}
        data['html_form'] = render_to_string('users/delete_user.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs['pk'])
        user.delete()
        data = dict()
        data['form_is_valid'] = True
        context = {
            'users': User.objects.order_by('username'),
            'perms': PermWrapper(self.request.user),
        }
        data['html_users'] = render_to_string('users/users.html', context)
        return JsonResponse(data)


# User Password Change View
class UserPasswordChangeView(PermissionRequiredMixin, FormView):
    template_name = "users/password_change.html"
    form_class = UserPasswordChangeForm
    permission_required = 'auth.change_user_password'
    raise_exception = True

    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs['pk'])
        context = {'user': user, 'user_password_change_form': UserPasswordChangeForm(),}
        data = dict()
        data['html_form'] = render_to_string('users/password_change.html', context, request=request)
        return JsonResponse(data)

    def form_valid(self, form):
        user = User.objects.get(id=self.kwargs['pk'])
        user.set_password(form.cleaned_data['new_password'])
        user.save()
        data = dict()
        data['form_is_valid'] = True
        context = {
            'users': User.objects.order_by('username'),
            'perms': PermWrapper(self.request.user),
        }
        data['html_users'] = render_to_string('users/users.html', context)
        return JsonResponse(data)

    def form_invalid(self, form):
        data = dict()
        data['form_is_valid'] = False
        data['form_errors'] = form.errors
        return JsonResponse(data)
