from django.db import models

from organisateur import Contact
from organisateur import Organisateur

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

    nom = models.CharField(max_length=200)
    organisateur = models.ForeignKey(Organisateur)
    lieu = models.CharField(max_length=400)
    debut = models.DateTimeField()
    fin = models.DateTimeField()

    objet = models.CharField(max_length=200)
    adresse = models.CharField(max_length=500)
    contact = models.ForeignKey(Contact)
    telephone = models.CharField(max_length=20)

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
