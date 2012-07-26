# -*- coding: utf-8 -*-
# vim: set ts=4

from django.conf.urls import patterns, include, url

urlpatterns = patterns('DUlSine.views.general',
    url(r'^(?P<delegation>\d+)/$', 'index', name='index')
)

urlpatterns += patterns('DUlSine.views.DPS',
    url(r'^(?P<delegation>\d+)/DPS/$', 'index', name='dps.index'),
    url(r'^(?P<delegation>\d+)/DPS/(?P<dps_id>\d+)/$', 'details', name='dps.details'),

    # Création d'un nouveau DPS.
    # Deux étapes distinctes :
    # * information sur l'organisateur et le DPS
    # * gestion des dimenssionnements
    url(r'^(?P<delegation>\d+)/DPS/nouveau/$', 'nouveau', name='dps.nouveau'),
    url(r'^(?P<delegation>\d+)/DPS/nouveau/(?P<dps_hash>\w+)/$', 'nouveau', name='dps.nouveau'),
    url(r'^(?P<delegation>\d+)/DPS/nouveau/(?P<dps_hash>\w+)/(?P<dim_id>\d+)/$', 'dimenssionnement', name='dps.nouveau.dimenssionnement'),

    # Calendrier au format CalDav
    # Deux arguments optionnels peuvent etre passés via l'url
    # * avant : ne retourne pas les événements de plus de 'avant' jours
    # * apres : ne retourne pas les événements dans plus de 'apres' jours
    url(r'^(?P<delegation>\d+)/DPS/calendrier(?:/(?P<avant>\d+)(?:/(?P<apres>\d+))?)?/$', 'calendrier', name='dps.calendrier'),
)

urlpatterns += patterns('DUlSine.views.benevole',
    url(r'^(?P<delegation>\d+)/benevole/$', 'index', name='benevole.index'),
    url(r'^benevole/(?P<benevole_id>\d+)/$', 'details', name='benevole.details'),
    url(r'^benevole/(?P<benevole_id>\d+)/calendrier(?:/(?P<event_type>\w+))?(?:/(?P<avant>\d+)(?:/(?P<apres>\d+))?)?/$', 'calendrier', name='benevole.calendrier'),
)
