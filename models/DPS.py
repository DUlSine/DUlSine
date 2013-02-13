# -*- coding: utf-8 -*-
# vim: set ts=4

from decimal import Decimal
import math
import os, binascii

from django.db import models
from django.db.models import Q

from structure import Structure
from organisateur import Organisateur
from benevole import Benevole

from dulsine_commons import *


def random_hash():
    """ Create a random string of size 15 """
    return binascii.b2a_hex(os.urandom(15))


class DPS(models.Model):
    class Meta:
        app_label = 'DUlSine'
        verbose_name_plural = 'DPS'

    hash_id = models.CharField(unique = True, max_length = 30, default = random_hash)
    structure = models.ForeignKey(Structure, null = True, blank = True)

    organisateur = models.ForeignKey(Organisateur)
    intitule = models.CharField(max_length = 200)
    objet = models.CharField(max_length = 200)

    lieu = models.CharField(max_length = 400)
    circuit = models.CharField(max_length = 1, choices = CIRCUITS, default = CIRCUITS[0][0])
    superficie = models.IntegerField()
    distance = models.IntegerField()
    risques = models.CharField(max_length = 200)

    adresse_rdv = models.CharField(max_length = 500)
    contact_sur_place_nom = models.CharField(max_length = 200)
    contact_sur_place_prenom = models.CharField(max_length = 200)
    contact_sur_place_civilite = models.CharField(max_length = 4, choices = CIVILITES, default = CIVILITES[0][0])
    contact_sur_place_telephone = models.CharField(max_length = 20)

    prix = models.IntegerField(default = 0)
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


class Dimensionnement(models.Model):
    class Meta:
        app_label = 'DUlSine'

    DPS = models.ForeignKey(DPS)

    # If the name is not given, the DPS name is used instead
    nom = models.CharField(max_length = 200, blank = True)
    debut = models.DateTimeField()
    fin = models.DateTimeField()

    effectifs_acteurs = models.IntegerField(default = 0)
    age_acteurs       = models.CharField(max_length = 50, blank = True)
    type_acteurs      = models.CharField(max_length = 1, choices = TYPES_ACTEURS, blank = True)

    effectifs_public    = models.IntegerField(default = 0)
    age_public          = models.CharField(max_length = 50, blank = True)
    besoins_specifiques = models.CharField(max_length = 200, blank = True)

    medecin = models.CharField(max_length = 200, blank = True)
    infirmier = models.BooleanField(default = False)
    ambulance_prive = models.BooleanField(default = False)
    secours_public = models.CharField(max_length = 200, blank = True)
    secours_autre = models.CharField(max_length = 200, blank = True)

    centre_sdis = models.CharField(max_length = 200)
    hopital = models.CharField(max_length = 200)

    repas = models.BooleanField()

    P2 = models.DecimalField(max_digits = 3, decimal_places = 2, choices = RISQUES_P2, default = RISQUES_P2[0][0])
    E1 = models.DecimalField(max_digits = 3, decimal_places = 2, choices = RISQUES_E1, default = RISQUES_E1[0][0])
    E2 = models.DecimalField(max_digits = 3, decimal_places = 2, choices = RISQUES_E2, default = RISQUES_E2[0][0])
    IS = models.IntegerField(null = True, blank = True)

    def __unicode__(self):
        if self.nom != None:
            return u"%s : %s" %(self.DPS, self.nom)
        else:
            return u"%s : %s - %s" %(self.DPS, self.debut, self.fin)

    def shortName(self):
        if self.nom != None:
            return self.nom
        else:
            return u"%s - %s" %(self.debut, self.fin)


    def getIndice(self):
        """
         Compute the risque indicator according to the law
          @return the indicator
        """
        return self.P2 + self.E1 + self.E2


    def calculRISPublic(self):
        return self.calculRIS(True)

    def calculRISActeur(self):
        return self.calculRIS(False)

    def calculRIS(self, public):
        """
         Compute the RIS (number of first aiders) according to the given informations
          @param public: True if the DPS is targetting the public. False for the actors.
          @return the RIS
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


    def calculISPublic(self):
        return self.calculIS(True)

    def calculISActeur(self):
        return self.calculIS(False)

    def calculIS(self, public):
        """
         Compute the minimal number of first aiders
          @param public: True if the DPS is targetting the public. False for the actors.
          @return the minimal number of first aiders
        """
        ris = self.calculRIS(public)
        if(ris <= 0.25):
            num_is = 0
        elif(ris <= 1.125):
            num_is = 2
            # A PAPS is not enough when protecting actors and if the public
            # helps took more than 30 minutes to come (E2 = 0.40)
            if(public == False or self.E2 == 0.40):
                num_is = 4
        elif(ris <= 4):
            num_is = 4
        else:
            num_is = math.ceil(ris)
            # Round to the nearest odd number (upper bound)
            if(num_is % 2 == 1):
                num_is += 1

        return num_is


    # Compute the required number of the given person
    def nombreISMax(self, formation):
        if(self.IS == None):
            return 0

        if(formation == DIPLOME_CI):
            return (self.IS - self.IS % 4) / 4
        elif(formation == DIPLOME_PSE2):
            return (self.IS - self.IS % 4) / 2 + (self.IS % 4) / 2
        elif(formation == DIPLOME_PSE1):
            return (self.IS - self.IS % 4) / 4 + (self.IS % 4) / 2
        elif(formation == DIPLOME_PSC1):
            return Team.objects.filter(dimensionnement = self, team_type = 1).count()
        else:
            assert(0)


    # Compute the current number of the given person
    def nombreIS(self, formation):
        return Inscription.objects.filter(team__dimensionnement = self, fonction = formation).count()


    # Compute the number of benevole marked as not available
    def nombreND(self):
        return Wish.objects.filter(dimensionnement = self, wish = WISH_ND).count()

    def nombreD(self):
        return Wish.objects.filter(dimensionnement = self).filter(~Q(wish = WISH_ND)).count()


from team import Team, Inscription, Wish
