# -*- coding: utf-8 -*-


from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import StaticPage
import json
from .forms import StaticPageForm


class StaticPageTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.credentials = {'username': 'user', 'password': 'password'}
        self.user = User.objects.create_user(**self.credentials)
        self.logged_in = self.client.login(**self.credentials)

    def test_valid_settings(self):
        self.assertTrue(self.user)
        self.assertTrue(self.logged_in)

    def test_static_page_crud(self):
        response = self.client.get(reverse("static_page:static_page_create"))
        self.assertEquals(response.status_code, 200)
        response = self.client.post(
            reverse("static_page:static_page_create"),
            data={
                'meta_title': 'TEST',
                'head': 'TEST',
                'body': 'TEST',
                'is_public': True,
                'created_at': timezone.now(),
                'updated_at': timezone.now()
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(StaticPage.objects.all().count(), 1)
        static_page_pk = str(StaticPage.objects.all()[0].pk)
        url = '/administration/static_page/' + static_page_pk + '/edit/'
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        response = self.client.post(
            url,
            {
                'meta_title': 'NEW TEST',
                'head': 'NEW TEST',
                'body': 'NEW TEST',
                'is_public': False,
                'created_at': timezone.now(),
                'updated_at': timezone.now()
            },
            follow=True
        )
        self.assertEquals(response.status_code, 200)
        all_static_pages = StaticPage.objects.all()
        self.assertEquals(all_static_pages.count(), 1)
        new_static_page = StaticPage.objects.first()
        self.assertEquals(new_static_page.head, 'NEW TEST')
        self.assertEquals(new_static_page.is_public, False)
        url = '/administration/static_page/' + static_page_pk + '/delete/'
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        response = self.client.post(url, data={'post': 'yes'}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(StaticPage.objects.all().count(), 0)

    def test_static_page_list(self):
        response = self.client.get(reverse("static_page:static_page_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'static_pages/static_pages.html')
        self.assertContains(response, 'Статические страницы')

    def test_static_page_sorting(self):
        first_static_page = StaticPage.objects.create(
            pk=150,
            idx=0,
            meta_title='First',
            head='First',
            body='First',
            is_public=True,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        second_static_page = StaticPage.objects.create(
            pk=160,
            idx=1,
            meta_title='Second',
            head='Second',
            body='Second',
            is_public=False,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        third_static_page = StaticPage.objects.create(
            pk=170,
            idx=2,
            meta_title='Third',
            head='Third',
            body='Third',
            is_public=False,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        data = {150: 2, 160: 0, 170: 1}
        response = self.client.post(
            reverse("static_page:static_page_sorting"),
            data=json.dumps(data),
            content_type='application/json;',
        )
        self.assertEqual(response.content.decode("utf-8"), '{"saved": "OK"}')
        self.assertEqual(response.status_code, 200)
        first_static_page.refresh_from_db()
        self.assertEquals(first_static_page.idx, 2)
        second_static_page.refresh_from_db()
        self.assertEquals(second_static_page.idx, 0)
        third_static_page.refresh_from_db()
        self.assertEquals(third_static_page.idx, 1)

    def test_static_page_form_valid(self):
        data = {
            'meta_title': 'TEST',
            'head': 'TEST',
            'body': 'TEST',
            'is_public': True
        }
        form = StaticPageForm(data=data)
        self.assertTrue(form.is_valid())
