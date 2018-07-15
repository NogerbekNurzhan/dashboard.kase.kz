# -*- coding: utf-8 -*-


from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from .views import UserCreateView, UserEditView, UserDeleteView, UserListView, UserPasswordChangeView


urlpatterns = [
	# User List
	url(r'^$',
		login_required(login_url=reverse_lazy('administration_login'))(UserListView.as_view()),
		name='user_list'),

	# User Create
	url(r'^create/$',
		UserCreateView.as_view(),
		name='user_create'),

	# User Delete
	url(r'^(?P<pk>\d+)/delete/$',
		UserDeleteView.as_view(),
		name='user_delete'),

	# User Edit
	url(r'^(?P<pk>\d+)/edit/$',
		UserEditView.as_view(),
		name='user_edit'),

	# User Password Change
	url(r'^(?P<pk>\d+)/password_change/$',
		UserPasswordChangeView.as_view(),
		name='user_password_change'),
]
