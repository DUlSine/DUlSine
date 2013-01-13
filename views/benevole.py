# -*- coding: utf-8 -*-
# vim: set ts=4
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from DUlSine.models import Structure, Benevole

def index(request, structure):
    Struct = get_object_or_404(Structure, numero = structure)
    benevoles = Benevole.objects.filter(structure = structure)

    return render_to_response('benevole/index.html', {'structure': Struct, 'benevoles': benevoles}, context_instance = RequestContext(request))



def details(request, benevole_id):
    return HttpResponse(status = 200)

def calendrier(request, benevole_id, event_type = None, avant = None, apres = None):
    return HttpResponse(status = 200)
