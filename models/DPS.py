# -*- coding: utf-8 -*-
# vim: set ts=4
from decimal import Decimal
import math
import os, binascii

from django.db import models

from delegation import Delegation
from organisateur import Organisateur, CIVILITES
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


def random_hash():
    """ Retourne une chaine aléatoire """
    return binascii.b2a_hex(os.urandom(15))


class DPS(models.Model):
    class Meta:
        app_label = 'DUlSine'

    hash_id = models.CharField(unique=True, max_length = 30, default = random_hash)
    delegation = models.ForeignKey(Delegation)

    organisateur = models.ForeignKey(Organisateur)
    intitule = models.CharField(max_length = 200)
    objet = models.CharField(max_length = 200)

    lieu = models.CharField(max_length=400)
    adresse_rdv = models.CharField(max_length = 500)
    contact_sur_place_nom = models.CharField(max_length=200)
    contact_sur_place_prenom = models.CharField(max_length=200)
    contact_sur_place_civilite = models.CharField(max_length=4, choices=CIVILITES, default=CIVILITES[0][0])
    contact_sur_place_telephone = models.CharField(max_length = 20)

    prix = models.IntegerField(null = True, blank = True)
    remarques = models.CharField(max_length = 500, blank = True)


    def __unicode__(self):
        return self.intitule


RISQUES_P2 = (
    ( Decimal("0.25"), 'Public Assis : spectacle, cérémonie culturelle, réunion publique'),
    ( Decimal("0.3"),  'Public debout : cérémonie culturelle, réunion publique,restauration, exposition, foire, salon, comice agricole, ..'),
    ( Decimal("0.35"), 'Public debout : spectacle avec public statique, fête foraine, rendez-vous sportif avec protection du public par rapport à l’évènement, ...'),
    ( Decimal("0.4"),  'Public debout : spectacle avec public dynamique, danse, féria, fête votive, carnaval, spectacle de rue, évènement se déroulant sur plusieurs jours avec présence permanente du public')
)

RISQUES_E1 = (
    ( Decimal("0.25"), 'Permanente (bâtiment, salle en dur,..) voies publics avec accès dégagés'),
    ( Decimal("0.3"),  'Non permanente (gradins, tribunes, chapiteaux,..) espace naturels ≤ 2 hectares, brancardage 150m <longueur ≤300m Terrain en pente sur plus de 100 m'),
    ( Decimal("0.35"), 'Espace naturels : 2 ha < surface ≤ 5 ha, brancardage 300m <longueur ≤600m, terrain en pente sur plus de 150m. Autres conditions d’accès difficile'),
    ( Decimal("0.4"),  'Espaces naturels : surface > 5 hectares - Brancardage : longueur > 600m. Terrain en pente sur plus de 300m autres conditions d\'accès difficiles. Progression des secours rendue difficile par la présence du public')
)

RISQUES_E2 = (
    ( Decimal("0.25"), '≤ 10 minutes'),
    ( Decimal("0.3"),  '> 10 minutes et ≤ 20 minutes'),
    ( Decimal("0.35"), '> 20 minutes et ≤ 30 minutes'),
    ( Decimal("0.4"),  '> 30 minutes')
)


class Dimenssionnement(models.Model):
    class Meta:
        app_label = 'DUlSine'

    DPS = models.ForeignKey(DPS)

    debut = models.DateTimeField()
    fin = models.DateTimeField()

    circuit = models.CharField(max_length = 1, choices = CIRCUITS, default = CIRCUITS[0][0])
    superficie = models.IntegerField()
    distance = models.IntegerField()
    risques = models.CharField(max_length=200)

    effectifs_acteurs = models.IntegerField()
    age_acteurs       = models.CharField(max_length=50, blank = True)
    type_acteurs      = models.CharField(max_length=1, choices=TYPES_ACTEURS, blank = True)

    effectifs_public    = models.IntegerField()
    age_public          = models.CharField(max_length=50, blank = True)
    besoins_specifiques = models.CharField(max_length=200, blank = True)

    medecin = models.CharField(max_length=200, blank = True)
    infirmier = models.BooleanField(default = False)
    ambulance_prive = models.BooleanField(default = False)
    secours_public = models.CharField(max_length=200, blank=True)
    secours_autre = models.CharField(max_length=200, blank=True)

    centre_sdis = models.CharField(max_length=200)
    hopital = models.CharField(max_length=200)

    repas = models.BooleanField()

    P2 = models.DecimalField(max_digits = 3, decimal_places = 2, choices = RISQUES_P2, default = RISQUES_P2[0][0])
    E1 = models.DecimalField(max_digits = 3, decimal_places = 2, choices = RISQUES_E1, default = RISQUES_E1[0][0])
    E2 = models.DecimalField(max_digits = 3, decimal_places = 2, choices = RISQUES_E2, default = RISQUES_E2[0][0])
    IS = models.IntegerField(null = True, blank = True)

    def __unicode__(self):
        return str(self.debut) + ' - ' + str(self.fin)

    def calculRIS(self, public):
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


    def calculIS(self, public):
        """
         Calcul le nombre d'IS minimum sur le DPS
          @params public: True si le DPS concerne le public, False pour les acteurs
          @return le nombre minimum d'IS pour le DPS.
        """
        ris = self.calculRIS(public)
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

    dimenssionnement = models.ForeignKey(Dimenssionnement)
    PSE2 = models.ForeignKey(Intervenant, related_name='PAPS_PSE2')
    PSE1 = models.ForeignKey(Intervenant, related_name='PAPS_PSE1')


class Equipe(models.Model):
    class Meta:
        app_label = 'DUlSine'

    dimenssionnement = models.ForeignKey(Dimenssionnement)
    CI     = models.ForeignKey(Intervenant, related_name='Equipe_CI')
    PSE2_1 = models.ForeignKey(Intervenant, related_name='Equipe_PSE2_1')
    PSE2_2 = models.ForeignKey(Intervenant, related_name='Equipe_PSE2_2')
    PSE1   = models.ForeignKey(Intervenant, related_name='Equipe_PSE1')
    PSC1   = models.ForeignKey(Intervenant, related_name='Equipe_PSC1', null=True, blank = True)


class Binome(models.Model):
    class Meta:
        app_label = 'DUlSine'

    dimenssionnement = models.ForeignKey(Dimenssionnement)
    Equipe = models.ForeignKey(Equipe)
    PSE2 = models.ForeignKey(Intervenant, related_name='Binome_PSE2')
    PSE1 = models.ForeignKey(Intervenant, related_name='Binome_PSE1')

