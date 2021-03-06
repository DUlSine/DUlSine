# -*- coding: utf-8 -*-
# vim: set ts=4

from django.contrib.auth.models import User
from django.db import models

from structure import Structure

from dulsine_commons import DIPLOME_CONDUCTEURS_LIST, DIPLOME_FORMATEURS_LIST, DIPLOME_SECOURS_LIST


class Benevole(models.Model):
    class Meta:
        app_label = 'DUlSine'
        ordering = ('user__last_name', 'user__first_name')

    def __unicode__(self):
        return u"%s (%s)" % (self.user.get_full_name(), self.structure.nom)

    user = models.OneToOneField(User)
    structure = models.ForeignKey(Structure, verbose_name='structure de ratachement')

    # TODO: use https://docs.djangoproject.com/en/dev/ref/contrib/localflavor/
    telephone = models.IntegerField('téléphone')
    adresse = models.CharField('adresse', max_length = 200)
    date_naissance = models.DateField('date de naissance')
    diplomes = models.CommaSeparatedIntegerField('diplômes', max_length = 200)

    def listDiplomes(self, lookup):
        diplomes = []
        for token in self.diplomes.split(','):
            token = int(token)
            if token in lookup:
                diplomes.append(lookup[token])
        return diplomes

    # Return the only diploma for 'Secours'
    def diplomesSecours(self):
        return self.listDiplomes(DIPLOME_SECOURS_LIST)

    # Return the list of diploma for 'Conducteurs'
    def diplomesConducteur(self):
        return self.listDiplomes(DIPLOME_CONDUCTEURS_LIST)

    # Return the list of diploma for 'Formateur'
    def diplomesFormateur(self):
        return self.listDiplomes(DIPLOME_FORMATEURS_LIST)
