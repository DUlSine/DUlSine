# -*- coding: utf-8 -*-
# vim: set ts=4

from django.contrib.auth.models import User
from django.db import models

from structure import Structure

class Benevole(models.Model):
    class Meta:
        app_label = 'DUlSine'

    def __unicode__(self):
        return u"%s (%s)" %(self.user.get_full_name(), self.structure.nom)

    user = models.OneToOneField(User)
    structure = models.ForeignKey(Structure, verbose_name='structure de ratachement')

    # TODO: use https://docs.djangoproject.com/en/dev/ref/contrib/localflavor/
    telephone = models.IntegerField('téléphone')
    adresse = models.CharField('adresse', max_length = 200)
    date_naissance = models.DateField('date de naissance')
    diplomes = models.CommaSeparatedIntegerField('diplômes', max_length = 200)
