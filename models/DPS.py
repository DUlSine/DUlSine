# -*- coding: utf-8 -*-
# vim: set ts=4
from django.db import models

from delegation import Delegation
from organisateur import Contact, Organisateur
from intervenant import Intervenant

CIRCUITS = (
        ('O', 'ouvert'),
        ('F', 'ferme'),
        ('N', 'pas de circuit')
    )

TYPES_ACTEURS = (
        ('P', 'Professionnels'),
        ('A', 'Amateurs'),
        ('M', 'Mixte')
)


class DPS(models.Model):
    class Meta:
        app_label = 'DUlSine'

    delegation = models.ForeignKey(Delegation)
    nom = models.CharField(max_length=200)
    organisateur = models.ForeignKey(Organisateur)

    objet = models.CharField(max_length=200)
    adresse = models.CharField(max_length=500)
    contact = models.ForeignKey(Contact)
    telephone = models.CharField(max_length=20)

    prix = models.IntegerField()
    remarques = models.CharField(max_length=500)


class Dimenssionnement(models.Model):
    class Meta:
        app_label = 'DUlSine'

    DPS = models.ForeignKey(DPS)

    debut = models.DateTimeField()
    fin = models.DateTimeField()
    lieu = models.CharField(max_length=400)

    circuit = models.CharField(max_length=1, choices=CIRCUITS)
    superficie = models.IntegerField()
    distance = models.IntegerField()
    risques = models.CharField(max_length=200)

    effectifs_acteurs = models.IntegerField()
    age_acteurs       = models.CharField(max_length=50)
    type_acteurs      = models.CharField(max_length=1, choices=TYPES_ACTEURS)

    effectifs_public    = models.IntegerField()
    age_public          = models.CharField(max_length=50)
    besoins_specifiques = models.CharField(max_length=200)

    medecin = models.ForeignKey(Contact, related_name='medecin', null=True)
    infirmier = models.BooleanField()
    ambulance_prive = models.BooleanField()
    secours_public = models.CharField(max_length=200, null=True)
    secours_autre = models.CharField(max_length=200, null=True)

    centre_sdis = models.CharField(max_length=200)
    hopital = models.CharField(max_length=200)

    repas = models.BooleanField()

    P2 = models.IntegerField()
    E1 = models.IntegerField()
    E2 = models.IntegerField()
    IS = models.IntegerField()


class PAPS(models.Model):
    class Meta:
        app_label = 'DUlSine'

    DPS = models.ForeignKey(DPS)
    PSE2 = models.ForeignKey(Intervenant, related_name='PAPS_PSE2')
    PSE1 = models.ForeignKey(Intervenant, related_name='PAPS_PSE1')


class Equipe(models.Model):
    class Meta:
        app_label = 'DUlSine'

    DPS = models.ForeignKey(DPS)
    CI     = models.ForeignKey(Intervenant, related_name='Equipe_CI')
    PSE2_1 = models.ForeignKey(Intervenant, related_name='Equipe_PSE2_1')
    PSE2_2 = models.ForeignKey(Intervenant, related_name='Equipe_PSE2_2')
    PSE1   = models.ForeignKey(Intervenant, related_name='Equipe_PSE1')
    PSC1   = models.ForeignKey(Intervenant, related_name='Equipe_PSC1', null=True)


class Binome(models.Model):
    class Meta:
        app_label = 'DUlSine'

    DPS = models.ForeignKey(DPS)
    Equipe = models.ForeignKey(Equipe)
    PSE2 = models.ForeignKey(Intervenant, related_name='Binome_PSE2')
    PSE1 = models.ForeignKey(Intervenant, related_name='Binome_PSE1')

