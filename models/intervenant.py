# -*- coding: utf-8 -*-
# vim: set ts=4
from django.db import models

from delegation import Delegation

class Intervenant(models.Model):
    class Meta:
        app_label = 'DUlSine'

    delegation = models.ForeignKey(Delegation)
