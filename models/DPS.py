# -*- coding: utf-8 -*-
# vim: set ts=4
import math

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

    # Déterminer la longeur du hash suivant l'algo choisi
    hash_id = models.CharField(max_length = 100)
    delegation = models.ForeignKey(Delegation)

    organisateur = models.ForeignKey(Organisateur)
    intitule = models.CharField(max_length = 200)
    objet = models.CharField(max_length = 200)

    adress_rdv = models.CharField(max_length = 500)
    contact_sur_place = models.ForeignKey(Contact)
    telephone_contact = models.CharField(max_length = 20)

    prix = models.IntegerField()
    remarques = models.CharField(max_length = 500)


    def __unicode__(self):
        return self.intitule



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

    def RIS(self, public):
        """
         Calcul le RIS suivant les informations disponible
          @param public: True si le DPS concerne le public, False pour les acteurs
          @return le RIS
        """
        indice = self.P2 + self.E1 + self.E2
        P = 0
        if(public):
            P = self.effectifs_public;
        else:
            P = self.effectifs_acteurs;

        if(P > 100000):
            P = 100000 + (P - 100000) / 2

        return indice * P / 1000


    def IS(self, public):
        """
         Calcul le nombre d'IS minimum sur le DPS
          @params public: True si le DPS concerne le public, False pour les acteurs
          @return le nombre minimum d'IS pour le DPS.
        """
        ris = self.RIS(public)
        if(ris <= 0.25):
            num_is = 0
        elif(ris <= 1.125):
            num_is = 2
            # Un PAPS n'est pas suffisant pour les acteurs ou dans le cas où
            # les secours public sont à plus de 30 minutes (E2 = 0.40)
            if(public == False or self.E2 == 0.40):
                num_is = 4
        elif(ris <= 4):
            num_is = 4
        else:
            num_is = math.ceil(ris)
            # Arrondis à l'entier pair supérieur
            if(num_is % 2 == 1):
                num_is += 1

        return num_is



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

