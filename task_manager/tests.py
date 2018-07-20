# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase


class TestAPI(TestCase):
    def test_api_get(self):
        self.assertEqual(1 + 1, 2)
