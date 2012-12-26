# -*- coding: utf-8 -*-
# vim: set ts=4

from django.conf.urls import patterns, include, url

urlpatterns = patterns('DUlSine.views.general',
    url(r'^$', 'index', name = 'index')
)

# Authentication
urlpatterns += patterns('django.contrib.auth.views',
    url(r'^accounts/login/$', 'login', name = 'accounts.login'),
    url(r'^accounts/logout/$', 'logout', {'template_name': 'registration/logged_out.html'}, name = 'accounts.logout'),#, {'template_name': 'template/registration/logged_out.html'}),
)

urlpatterns += patterns('DUlSine.views.DPS',
    url(r'^(?P<structure>\d+)/DPS/$', 'index', name = 'dps.index'),
    url(r'^(?P<structure>\d+)/DPS/(?P<dim_id>\d+)/$', 'details', name = 'dimensionnement.details'),

    # Creating a new DPS in  steps:
    # * information on the organizer and on the DPS
    #  * loop between 'modification' and 'verification'
    # * list of every days
    # * adding a new day
    # * looping between 'modification' and 'verification'
    url(r'^DPS/demande/$', 'demande', name = 'dps.demande'),
    url(r'^DPS/demande/(?P<dps_hash>[0-9a-f]+)/$', 'demande_details', name = 'dps.demande.details'),
    url(r'^DPS/demande/(?P<dps_hash>[0-9a-f]+)/verification/$', 'demande_verification', name = 'dps.demande.verification'),
    url(r'^DPS/demande/(?P<dps_hash>[0-9a-f]+)/modification/$', 'demande_modification', name = 'dps.demande.modification'),
    url(r'^DPS/demande/(?P<dps_hash>[0-9a-f]+)/dimensionnement/$', 'dimensionnement', name = 'dps.demande.dimensionnement'),
    url(r'^DPS/demande/(?P<dps_hash>[0-9a-f]+)/dimensionnement/(?P<dim_id>\d+)/verification/$', 'dimensionnement_verification', name = 'dps.demande.dimensionnement.verification'),
    url(r'^DPS/demande/(?P<dps_hash>[0-9a-f]+)/dimensionnement/(?P<dim_id>\d+)/modification/$', 'dimensionnement_modification', name = 'dps.demande.dimensionnement.modification'),

    # Managing DPS
    url(r'^(?P<structure>\d+)/admin/DPS/$', 'admin_index', name = 'dps.admin.index'),
    url(r'^(?P<structure>\d+)/admin/DPS/(?P<dps_id>\d+)/$', 'admin_details', name = 'dps.admin.details'),
    url(r'^(?P<structure>\d+)/admin/DPS/(?P<dps_id>\d+)/(?P<dim_id>\d+)/$', 'admin_dimensionnement', name = 'dps.admin.dimensionnement.details'),
    url(r'^(?P<structure>\d+)/admin/DPS/(?P<dps_id>\d+)/devis/$', 'devis', name = 'dps.admin.devis'),

    # Calendars in CalDav format
    # Two optional arguments given throug the url:
    # * avant : only return events that happend less than 'avant' days before
    # * apres : do not return events in more than 'apres' days
    url(r'^(?P<structure>\d+)/DPS/calendrier(?:/(?P<avant>\d+)(?:/(?P<apres>\d+))?)?/$', 'calendrier', name = 'dps.calendrier'),
)

urlpatterns += patterns('DUlSine.views.benevole',
    url(r'^(?P<structure>\d+)/benevoles/$', 'index', name = 'benevole.index'),
    url(r'^benevole/(?P<benevole_id>\d+)/$', 'details', name = 'benevole.details'),
    url(r'^benevole/(?P<benevole_id>\d+)/calendrier(?:/(?P<event_type>\w+))?(?:/(?P<avant>\d+)(?:/(?P<apres>\d+))?)?/$', 'calendrier', name = 'benevole.calendrier'),
)
