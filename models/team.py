# -*- coding: utf-8 -*-
# vim: set ts=4
from django.db import models

from benevole import Benevole
from DPS import Dimensionnement


TEAM_TYPES = (
    (0, 'PAPS'),
    (1, 'Equipe'),
    (2, 'Binome'),
    (3, 'Equipe d\'Evacuation')
)


FORMATIONS = (
    ('CI',      'Chef d\'Intervention'),
    ('PSE2',    'Equipier Secouriste'),
    ('PSE1',    'Secouriste'),
    ('PSC1',    'Sauveteur'),
    ('IPS',     'IPS'),

    ('CH',      'Chauffeur'),
    ('CHA',     'Chauffeur Ambulance')
)



class Team(models.Model):
    class Meta:
        app_label = 'DUlSine'

    dimensionnement = models.ForeignKey(Dimensionnement)
    team_type = models.IntegerField(choices = TEAM_TYPES)
    taille = models.IntegerField()

    def __unicode__(self):
        return u"%s (%s)" %(self.dimensionnement, TEAM_TYPES[self.team_type][1])



class Souhait(models.Model):
    class Meta:
        app_label = 'DUlSine'

    benevole = models.ForeignKey(Benevole)
    dimensionnement = models.ForeignKey(Dimensionnement)
    fonction = models.CharField(max_length = 6, choices = FORMATIONS)
    date = models.DateTimeField(auto_now_add = True)

    def __unicode__(self):
        return u"%s => %s : %s" %(self.dimensionnement,  self.fonction, self.benevole)



class Inscription(models.Model):
    class Meta:
        app_label = 'DUlSine'

    benevole = models.ForeignKey(Benevole)
    team = models.ForeignKey(Team)
    fonction = models.CharField(max_length = 6, choices = FORMATIONS)

    def __unicode__(self):
        return u"%s => %s : %s" %(self.team, self.fonction, self.benevole)

