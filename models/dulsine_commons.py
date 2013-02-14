# -*- coding: utf-8 -*-
# vim: set ts=4

# Common enumerations used in some places

CIVILITES = (
    ('M.', 'Monsieur'),
    ('Mme', 'Madame'),
    ('Mlle', 'Mademoiselle')
)


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


TEAM_TYPES = (
    (0, 'PAPS'),
    (1, 'Equipe'),
    (2, 'Binome'),
    (3, 'Equipe d\'Evacuation')
)


DIPLOME_CI = 0
DIPLOME_PSE2 = 1
DIPLOME_PSE1 = 2
DIPLOME_PSC1 = 3
DIPLOME_IPS = 4
DIPLOME_CDPE = 5

DIPLOME_SECOURS = (
    (DIPLOME_CI,   'CI'),
    (DIPLOME_PSE2, 'PSE2'),
    (DIPLOME_PSE1, 'PSE1'),
    (DIPLOME_PSC1, 'PSC1'),
    (DIPLOME_IPS, 'IPS'),

    (DIPLOME_CDPE, 'CDPE')
)

DIPLOME_SECOURS_LIST = { k:v for (k, v) in DIPLOME_SECOURS }


DIPLOME_CONDUCTEURS = (
    (10, 'CH'),
    (11, 'CHA'),
    (12, '4x4')
)
DIPLOME_CONDUCTEURS_LIST = { k:v for (k, v) in DIPLOME_CONDUCTEURS }


DIPLOME_FORMATEURS = (
    (20, 'FCI'),
    (21, 'PAE1'),
    (22, 'PAE2'),
    (23, 'PAE3'),
    (24, 'PAE4'),
)
DIPLOME_FORMATEURS_LIST = { k:v for (k, v) in DIPLOME_FORMATEURS }


FORMATIONS = DIPLOME_SECOURS + DIPLOME_CONDUCTEURS + DIPLOME_FORMATEURS


WISH_ND = 0

WISH_CHOICES = (
    (WISH_ND, 'N.D.'),
    (1, 'Disponible'),
    (2, 'Intéressé'),
    (3, 'Très intéressé'),
)

