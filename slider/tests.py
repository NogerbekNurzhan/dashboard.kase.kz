# -*- coding: utf-8 -*-


from django.test import TestCase, Client
from .models import Slide
from .forms import SlideForm
from django.urls import reverse
from django.contrib.auth.models import User
from CA.settings import BASE_DIR
import json
import os
import tempfile
import shutil
from django.test import override_settings
from django.core.files.uploadedfile import SimpleUploadedFile


IMAGE_PATH = tempfile.mkdtemp(dir=os.path.join(BASE_DIR, 'media_root'))


@override_settings(MEDIA_ROOT=IMAGE_PATH)
class SlideTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.credentials = {'username': 'user', 'password': 'password'}
        self.user = User.objects.create_user(**self.credentials)
        self.logged_in = self.client.login(**self.credentials)
        self.first_test_image = open(
            os.path.join(BASE_DIR, 'static/images/tests/test_image_1.jpg'), "r"
        )
        self.second_test_image = open(
            os.path.join(BASE_DIR, 'static/images/tests/test_image_2.jpg'), "r"
        )

    def test_valid_settings(self):
        self.assertTrue(self.user)
        self.assertTrue(self.logged_in)

    def test_slide_crud(self):
        response = self.client.get(reverse("slider:slide_create"))
        self.assertEquals(response.status_code, 200)
        response = self.client.post(
            reverse("slider:slide_create"),
            data={
                'head': 'TEST',
                'opt_head': 'TEST',
                'body': 'TEST',
                'location': 1,
                'public': True,
                'idx': 0,
                'image': self.first_test_image
            },
            follow=True,
            format='multipart'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Slide.objects.all().count(), 1)
        create_image = Slide.objects.first().image
        slide_pk = str(Slide.objects.all()[0].pk)
        url = '/administration/slide/' + slide_pk + '/edit/'
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        response = self.client.post(
            url,
            data={
                'head': 'NEW TEST',
                'opt_head': 'NEW TEST',
                'body': 'NEW TEST',
                'location': 2,
                'public': False,
                'image': self.second_test_image
            },
            follow=True,
            format='multipart'
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Slide.objects.all().count(), 1)
        self.assertEquals(Slide.objects.first().head, 'NEW TEST')
        self.assertEquals(Slide.objects.first().public, False)
        self.assertEquals(Slide.objects.first().public, False)
        edit_image = Slide.objects.first().image
        self.assertNotEqual(edit_image, create_image)
        url = '/administration/slide/' + slide_pk + '/delete/'
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        response = self.client.post(url, data={'post': 'yes'}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Slide.objects.all().count(), 0)

    def test_slide_list(self):
        response = self.client.get(reverse("slider:slide_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'slider/slides.html')
        self.assertContains(response, 'Слайды')

    def test_slide_form_valid(self):
        data = {
            'head': 'Custom TEXT',
            'opt_head': 'Custom TEXT',
            'body': 'Custom TEXT',
            'location': 1,
            'public': True,
        }
        files_data = {
            'image': SimpleUploadedFile(
                name=self.second_test_image.name,
                content=self.second_test_image.read(),
                content_type='image/jpeg'
            )
        }
        form = SlideForm(data=data, files=files_data)
        self.assertTrue(form.is_valid())

    def test_slide_sorting(self):
        first_slide = Slide.objects.create(
            pk=150,
            idx=0,
            head='First',
            opt_head='First',
            body='First',
            location=1,
            public=False,
            image=SimpleUploadedFile(
                name=self.first_test_image.name,
                content=self.first_test_image.read(),
                content_type='image/jpeg'
            )
        )
        second_slide = Slide.objects.create(
            pk=160,
            idx=1,
            head='Second',
            opt_head='Second',
            body='Second',
            location=2,
            public=False,
            image=SimpleUploadedFile(
                name=self.first_test_image.name,
                content=self.first_test_image.read(),
                content_type='image/jpeg'
            )
        )
        third_slide = Slide.objects.create(
            pk=170,
            idx=2,
            head='Third',
            opt_head='Third',
            body='Third',
            location=2,
            public=True,
            image=SimpleUploadedFile(
                name=self.first_test_image.name,
                content=self.first_test_image.read(),
                content_type='image/jpeg'
            )
        )
        data = {150: 2, 160: 0, 170: 1}
        response = self.client.post(
            reverse("slider:slide_sorting"),
            data=json.dumps(data),
            content_type='application/json;',
            follow=True
        )
        self.assertEqual(response.content.decode("utf-8"), '{"saved": "OK"}')
        self.assertEqual(response.status_code, 200)
        first_slide.refresh_from_db()
        self.assertEquals(first_slide.idx, 2)
        second_slide.refresh_from_db()
        self.assertEquals(second_slide.idx, 0)
        third_slide.refresh_from_db()
        self.assertEquals(third_slide.idx, 1)
        fileList = os.listdir(IMAGE_PATH)
        for fileName in fileList:
            shutil.rmtree(IMAGE_PATH + "/" + fileName)
        os.rmdir(IMAGE_PATH)
