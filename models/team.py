# -*- coding: utf-8 -*-
# vim: set ts=4

from django.core.mail import EmailMessage
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from dulsine_commons import TEAM_TYPES, DIPLOME_SECOURS, WISH_CHOICES, WISH_ND
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

    def get_simple_text(self):
        if self.wish == WISH_ND:
            return 'indisponible'
        else:
            return 'disponible'


# Callback that send a mail when a wish is done
@receiver(post_save, sender = Wish)
def wish_callback(sender, **kwargs):
    # TODO: add a Reply-To to help users
    # TODO: add the right person in Cc
    # TODO: set the From field
    wish = kwargs['instance']
    msg = EmailMessage(subject = '[DUlSine: %s] %s' %(wish.get_simple_text(), wish.dimensionnement),
                       body = render_to_string('dps/wish.email',
                                        {'dim': wish.dimensionnement,
                                         'user': wish.benevole.user,
                                         'wish': wish}),
                       to = [wish.benevole.user.email])
    msg.send(fail_silently = False)



class Inscription(models.Model):
    class Meta:
        app_label = 'DUlSine'

    benevole = models.ForeignKey(Benevole)
    team = models.ForeignKey(Team)
    fonction = models.IntegerField(choices = DIPLOME_SECOURS)

    def __unicode__(self):
        return u"%s => %s : %s" %(self.team, self.get_fonction_display(), self.benevole)

