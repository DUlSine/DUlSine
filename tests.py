# -*- coding: utf-8 -*-
# vim: set ts=4
from django.utils import unittest
from django.test.client import Client

from DUlSine.models.DPS import Dimenssionnement


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


class DimenssionnementTest(unittest.TestCase):
    def nouveau_dimenssionnement(self, effectif, public, P2, E1, E2):
        dim = Dimenssionnement()
        if(public):
            dim.effectifs_acteurs = 0
            dim.effectifs_public = effectif
        else:
            dim.effectifs_acteurs = effectif
            dim.effectifs_public = 0

        dim.P2 = P2
        dim.E1 = E1
        dim.E2 = E2
        return dim


    def test_RIS(self):
        self.assertEqual(self.nouveau_dimenssionnement(0, True, 0.25, 0.25, 0.25).RIS(True), 0)
        self.assertEqual(self.nouveau_dimenssionnement(0, False, 0.25, 0.25, 0.25).RIS(False), 0)
        self.assertEqual(self.nouveau_dimenssionnement(0, False, 0.25, 0.25, 0.25).RIS(True), 0)

        self.assertEqual(self.nouveau_dimenssionnement(1000, True, 0.25, 0.25, 0.25).RIS(True), 0.75)
        self.assertEqual(self.nouveau_dimenssionnement(2000, True, 0.25, 0.25, 0.25).RIS(True), 0.75 * 2)
        self.assertEqual(self.nouveau_dimenssionnement(10000, True, 0.25, 0.25, 0.25).RIS(True), 0.75 * 10)
        self.assertEqual(self.nouveau_dimenssionnement(100000, True, 0.25, 0.25, 0.25).RIS(True), 0.75 * 100)
        self.assertEqual(self.nouveau_dimenssionnement(101000, True, 0.25, 0.25, 0.25).RIS(True), 0.75 * (100 + 0.5))
        self.assertEqual(self.nouveau_dimenssionnement(102000, True, 0.25, 0.25, 0.25).RIS(True), 0.75 * (100 + 1))

        self.assertEqual(self.nouveau_dimenssionnement(1000, False, 0.25, 0.25, 0.25).RIS(False), 0.75)
        self.assertEqual(self.nouveau_dimenssionnement(2000, False, 0.25, 0.25, 0.25).RIS(False), 0.75 * 2)
        self.assertEqual(self.nouveau_dimenssionnement(10000, False, 0.25, 0.25, 0.25).RIS(False), 0.75 * 10)
        self.assertEqual(self.nouveau_dimenssionnement(100000, False, 0.25, 0.25, 0.25).RIS(False), 0.75 * 100)
        self.assertEqual(self.nouveau_dimenssionnement(101000, False, 0.25, 0.25, 0.25).RIS(False), 0.75 * (100 + 0.5))
        self.assertEqual(self.nouveau_dimenssionnement(102000, False, 0.25, 0.25, 0.25).RIS(False), 0.75 * (100 + 1))

        self.assertEqual(self.nouveau_dimenssionnement(1000, False, 0.30, 0.25, 0.25).RIS(False), 0.30 + 0.25 + 0.25)
        self.assertEqual(self.nouveau_dimenssionnement(1000, False, 0.35, 0.25, 0.25).RIS(False), 0.35 + 0.25 + 0.25)
        self.assertEqual(self.nouveau_dimenssionnement(1000, False, 0.40, 0.25, 0.25).RIS(False), 0.40 + 0.25 + 0.25)
        self.assertEqual(self.nouveau_dimenssionnement(1000, False, 0.40, 0.30, 0.25).RIS(False), 0.40 + 0.30 + 0.25)
        self.assertEqual(self.nouveau_dimenssionnement(1000, False, 0.40, 0.35, 0.25).RIS(False), 0.40 + 0.35 + 0.25)
        self.assertEqual(self.nouveau_dimenssionnement(1000, False, 0.40, 0.40, 0.25).RIS(False), 0.40 + 0.40 + 0.25)
        self.assertEqual(self.nouveau_dimenssionnement(1000, False, 0.40, 0.40, 0.30).RIS(False), 0.40 + 0.40 + 0.30)
        self.assertEqual(self.nouveau_dimenssionnement(1000, False, 0.40, 0.40, 0.35).RIS(False), 0.40 + 0.40 + 0.35)
        self.assertEqual(self.nouveau_dimenssionnement(1000, False, 0.40, 0.40, 0.40).RIS(False), 0.40 + 0.40 + 0.40)


    def test_IS(self):
        self.assertEqual(self.nouveau_dimenssionnement(0, True, 0.25, 0.25, 0.25).IS(True), 0)
        self.assertEqual(self.nouveau_dimenssionnement(250, True, 0.40, 0.35, 0.25).IS(True), 0)
        self.assertEqual(self.nouveau_dimenssionnement(251, True, 0.40, 0.35, 0.25).IS(True), 2)
        self.assertEqual(self.nouveau_dimenssionnement(1125, True, 0.40, 0.35, 0.25).IS(True), 2)
        self.assertEqual(self.nouveau_dimenssionnement(1126, True, 0.40, 0.35, 0.25).IS(True), 4)
        self.assertEqual(self.nouveau_dimenssionnement(2450, True, 0.40, 0.35, 0.25).IS(True), 4)
        self.assertEqual(self.nouveau_dimenssionnement(4000, True, 0.40, 0.35, 0.25).IS(True), 4)
        self.assertEqual(self.nouveau_dimenssionnement(4001, True, 0.40, 0.35, 0.25).IS(True), 6)
        self.assertEqual(self.nouveau_dimenssionnement(5001, True, 0.40, 0.35, 0.25).IS(True), 6)
        self.assertEqual(self.nouveau_dimenssionnement(6001, True, 0.40, 0.35, 0.25).IS(True), 8)

        # Un PAPS n'est pas suffisant si les secours pubic sont à plus de 30 minutes
        self.assertEqual(self.nouveau_dimenssionnement(251, True, 0.25, 0.35, 0.40).IS(True), 4)
        # Un PAPS n'est pas adapté pour les acteurs
        self.assertEqual(self.nouveau_dimenssionnement(251, False, 0.40, 0.35, 0.25).IS(False), 4)
