from django.db import models

class Delegation(models.Model):
    class Meta:
        app_label = 'DUlSine'

    nom = models.CharField(max_length = 50)
    adresse = models.CharField(max_length = 500)
