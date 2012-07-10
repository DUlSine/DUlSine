from django.db import models

from delegation import Delegation

class Intervenant(models.Model):
    class Meta:
        app_label = 'DUlSine'

    delegation = models.ForeignKey(Delegation)
