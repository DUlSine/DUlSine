# -*- coding: utf-8 -*-
# vim: set ts=4
from django.db import models

from structure import Structure

class Intervenant(models.Model):
    class Meta:
        app_label = 'DUlSine'

    structure = models.ForeignKey(Structure)
