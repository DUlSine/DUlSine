# -*- coding: utf-8 -*-
# vim: set ts=4
from django.db import models


class Structure(models.Model):
    class Meta:
        app_label = 'DUlSine'
        ordering = ('numero', )

    numero = models.IntegerField(primary_key = True)
    nom = models.CharField(max_length = 50)
    adresse = models.CharField(max_length = 500)
    parent = models.ForeignKey('Structure', null = True, blank = True)

    def __unicode__(self):
        return u"%d : %s" % (self.numero, self.nom)
