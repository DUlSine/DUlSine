from django.contrib.auth.models import User
from django.db import models

from structure import Structure

class Benevole(models.Model):
    class Meta:
        app_label = 'DUlSine'

    def __unicode__(self):
        return self.user.get_full_name() + ' (' + self.structure.nom + ')'

    user = models.OneToOneField(User)
    structure = models.ForeignKey(Structure)

    # TODO: use https://docs.djangoproject.com/en/dev/ref/contrib/localflavor/
    telephone = models.IntegerField()
    adresse = models.CharField(max_length = 200)
    date_naissance = models.DateField()
    diplomes = models.CommaSeparatedIntegerField(max_length = 200)
