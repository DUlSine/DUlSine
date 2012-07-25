# -*- coding: utf-8 -*-
# vim: set ts=4
from django.db import models

CIVILITES= (
    ('M.', 'Monsieur'),
    ('Mme', 'Madame'),
    ('Mlle', 'Mademoiselle')
)


class Organisateur(models.Model):
    class Meta:
        app_label = 'DUlSine'

    nom = models.CharField(max_length = 200)
    adresse = models.CharField(max_length = 500)

    contact_nom = models.CharField(max_length=200)
    contact_prenom = models.CharField(max_length=200)
    contact_civilite = models.CharField(max_length=4, choices=CIVILITES, default=CIVILITES[0][0])
    contact_fonction = models.CharField(max_length=200)

    representant_nom = models.CharField(max_length=200)
    representant_prenom = models.CharField(max_length=200)
    representant_civilite = models.CharField(max_length=4, choices=CIVILITES, default=CIVILITES[0][0])
    representant_fonction = models.CharField(max_length=200)

    telephone = models.CharField(max_length = 20, blank=True)
    portable = models.CharField(max_length = 20, blank=True)
    fax = models.CharField(max_length = 20, blank=True)
    email = models.EmailField(max_length = 100)

    def __unicode__(self):
        return self.nom
