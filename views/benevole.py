# -*- coding: utf-8 -*-
# vim: set ts=4
from django.http import HttpResponse

def index(request, delegation):
    return HttpResponse(status=200)

def details(request, benevole_id):
    return HttpResponse(status=200)

def calendrier(request, benevole_id, event_type=None, avant=None, apres=None):
    return HttpResponse(status=200)
