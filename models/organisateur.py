# -*- coding: utf-8 -*-
# vim: set ts=4
from django.db import models

CIVILITES= (
    ('M.', 'Monsieur'),
    ('Mme', 'Madame'),
    ('Mlle', 'Mademoiselle')
)

class Contact(models.Model):
    class Meta:
        app_label = 'DUlSine'

    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    civilite = models.CharField(max_length=4, choices=CIVILITES)
    fonction = models.CharField(max_length=200)

    def __unicode__(self):
        return self.civilite + " " + self.nom + " " + self.prenom



class Organisateur(models.Model):
    class Meta:
        app_label = 'DUlSine'

    nom = models.CharField(max_length = 200)
    adresse = models.CharField(max_length = 500)

    contact = models.ForeignKey(Contact, related_name='contact')
    representant = models.ForeignKey(Contact, related_name='representant')

    telephone = models.CharField(max_length = 20, blank=True)
    portable = models.CharField(max_length = 20, blank=True)
    fax = models.CharField(max_length = 20, blank=True)
    email = models.EmailField(max_length = 100)

    def __unicode__(self):
        return self.nom
