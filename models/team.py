# -*- coding: utf-8 -*-
# vim: set ts=4

from django.db import models
from dulsine_commons import TEAM_TYPES, DIPLOME_SECOURS, WISH_CHOICES

from benevole import Benevole
from DPS import Dimensionnement



class Team(models.Model):
    class Meta:
        app_label = 'DUlSine'

    dimensionnement = models.ForeignKey(Dimensionnement)
    team_type = models.IntegerField(choices = TEAM_TYPES)
    taille = models.IntegerField()

    def __unicode__(self):
        return u"%s (%s)" %(self.dimensionnement, self.get_team_type_display())



class Wish(models.Model):
    class Meta:
        app_label = 'DUlSine'
        verbose_name_plural = 'Wishes'

    benevole = models.ForeignKey(Benevole)
    dimensionnement = models.ForeignKey(Dimensionnement)
    wish = models.IntegerField(choices = WISH_CHOICES)
    date = models.DateTimeField(auto_now_add = True)

    def __unicode__(self):
        return u"%s => %s : %s" %(self.dimensionnement, self.benevole, self.get_wish_display())



class Inscription(models.Model):
    class Meta:
        app_label = 'DUlSine'

    benevole = models.ForeignKey(Benevole)
    team = models.ForeignKey(Team)
    fonction = models.IntegerField(choices = DIPLOME_SECOURS)

    def __unicode__(self):
        return u"%s => %s : %s" %(self.team, self.get_fonction_display(), self.benevole)

