# -*- coding: utf-8 -*-
# vim: set ts=4
from django.utils import unittest
from django.test.client import Client


class URLTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_DPS(self):
        self.assertEqual(self.client.get('/DUlSine/DPS/').status_code, 404)

        self.assertEqual(self.client.get('/DUlSine/38/DPS').status_code, 301)
        self.assertEqual(self.client.get('/DUlSine/38/DPS').status_code, 301)
        self.assertEqual(self.client.get('/DUlSine/arrt/DPS/').status_code, 404)

        self.assertEqual(self.client.get('/DUlSine/3802/DPS/123456').status_code, 301)
        self.assertEqual(self.client.get('/DUlSine/3802/DPS/123456/').status_code, 200)
        self.assertEqual(self.client.get('/DUlSine/3802/DPS/12razt/').status_code, 404)

        self.assertEqual(self.client.get('/DUlSine/3802/DPS/nouveau').status_code, 301)
        self.assertEqual(self.client.get('/DUlSine/3802/DPS/nouveau/').status_code, 200)
        self.assertEqual(self.client.get('/DUlSine/3802/DPS/nouveau/123456ref1231').status_code, 301)
        self.assertEqual(self.client.get('/DUlSine/3802/DPS/nouveau/123456ref1231/').status_code, 200)

        self.assertEqual(self.client.get('/DUlSine/3802/DPS/calendrier').status_code, 301)
        self.assertEqual(self.client.get('/DUlSine/3802/DPS/calendrier/').status_code, 200)
        self.assertEqual(self.client.get('/DUlSine/3802/DPS/calendrier/1258').status_code, 301)
        self.assertEqual(self.client.get('/DUlSine/3802/DPS/calendrier/1258/').status_code, 200)
        self.assertEqual(self.client.get('/DUlSine/3802/DPS/calendrier/562/981').status_code, 301)
        self.assertEqual(self.client.get('/DUlSine/3802/DPS/calendrier/562/981/').status_code, 200)
        self.assertEqual(self.client.get('/DUlSine/3802/DPS/calendrier/562/981/').status_code, 200)
        self.assertEqual(self.client.get('/DUlSine/3802/DPS/calendrier/562/981/re').status_code, 404)
        self.assertEqual(self.client.get('/DUlSine/3802/DPS/calendrier/562/981/123').status_code, 404)

    def test_benevole(self):
        self.assertEqual(self.client.get('/DUlSine/1230/benevole').status_code, 301)
        self.assertEqual(self.client.get('/DUlSine/1230/benevole/').status_code, 200)

        self.assertEqual(self.client.get('/DUlSine/benevole/calendrier').status_code, 404)
        self.assertEqual(self.client.get('/DUlSine/benevole/4212/calendrier').status_code, 301)
        self.assertEqual(self.client.get('/DUlSine/benevole/4212/calendrier/').status_code, 200)
        self.assertEqual(self.client.get('/DUlSine/benevole/4212/calendrier/format').status_code, 301)
        self.assertEqual(self.client.get('/DUlSine/benevole/4212/calendrier/format/').status_code, 200)
        self.assertEqual(self.client.get('/DUlSine/benevole/4212/calendrier/format/4567').status_code, 301)
        self.assertEqual(self.client.get('/DUlSine/benevole/4212/calendrier/format/4567/12').status_code, 301)
        self.assertEqual(self.client.get('/DUlSine/benevole/4212/calendrier/format/4567/12/').status_code, 200)
        self.assertEqual(self.client.get('/DUlSine/benevole/4212/calendrier/format/4567/12/12').status_code, 404)
        self.assertEqual(self.client.get('/DUlSine/benevole/4212/calendrier/format/4567/12/erat').status_code, 404)
