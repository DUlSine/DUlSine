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


DIPLOME_SECOURS = (
    (0, 'N.D.'),
    (1, 'CI'),
    (2, 'PSE2'),
    (3, 'PSE1'),
    (4, 'PSC1'),
    (5, 'IPS'),

    (6, 'CDPE')
)

NOT_AVAILABLE = 0
DIPLOME_CI = 1
DIPLOME_PSE2 = 2
DIPLOME_PSE1 = 3
DIPLOME_PSC1 = 4

DIPLOME_CONDUCTEURS = (
    (10, 'CH'),
    (11, 'CHA'),
    (12, '4x4')
)

DIPLOME_FORMATEURS = (
    (20, 'FCI'),
    (21, 'PAE1'),
    (22, 'PAE2'),
    (23, 'PAE3'),
    (24, 'PAE4'),
)

FORMATIONS = DIPLOME_SECOURS + DIPLOME_CONDUCTEURS + DIPLOME_FORMATEURS



