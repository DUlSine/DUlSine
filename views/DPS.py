# -*- coding: utf-8 -*-
# vim: set ts=4
from django.http import HttpResponse

def index(request, delegation):
    return HttpResponse(status=200)

def details(request, delegation, dps_id):
    return HttpResponse(status=200)

def nouveau(request, delegation, dps_hash=None, dimenssionnement=None):
    return HttpResponse(status=200)

def calendrier(request, delegation, avant=None, apres=None):
    return HttpResponse(status=200)
