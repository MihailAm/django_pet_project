from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from man.models import Man


class GetPagesTestCase(TestCase):
    fixtures = ['man_man.json', 'man_category.json', 'man_wife.json', 'man_tagpost.json']

    def setUp(self):
        """"""

    def test_mainpage(self):
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('man/index.html', response.template_name)
        self.assertEqual(response.context_data['title'], "Главная страница")

    def test_data_mainpage(self):
        m = Man.published.all().select_related('cat')
        path = reverse('home')
        response = self.client.get(path)
        self.assertQuerySetEqual(response.context_data['posts'], m[:3])

    def test_paginate_mainpage(self):
        path = reverse('home')
        page = 2
        paginate_by = 3
        response = self.client.get(path + f"?page={page}")
        m = Man.published.all().select_related('cat')
        self.assertQuerySetEqual(response.context_data['posts'], m[(page - 1) * paginate_by:page * paginate_by])

    def test_content_post(self):
        m = Man.published.get(pk=1)
        path = reverse('post', args=[m.slug])
        response = self.client.get(path)
        self.assertEqual(m.content, response.context_data['post'].content)

    def tearDown(self):
        """"""
