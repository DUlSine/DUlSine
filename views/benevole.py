# -*- coding: utf-8 -*-
# vim: set ts=4
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ModelForm
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from DUlSine.models import Structure, Benevole

import sys


class BenevoleForm(ModelForm):
    class Meta:
        model = Benevole
        exclude = ("user",)

class DUlSineUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", \
                  "username", "password1", "password2")


def index(request, structure):
    Struct = get_object_or_404(Structure, numero = structure)
    benevoles = Benevole.objects.filter(structure = structure)

    return render_to_response('benevole/index.html', {'structure': Struct, 'benevoles': benevoles}, context_instance = RequestContext(request))



def details(request, benevole_id):
    benevole = get_object_or_404(Benevole, id = benevole_id)

    return render_to_response('benevole/details.html', {'benevole': benevole}, context_instance = RequestContext(request))



def calendrier(request, benevole_id, event_type = None, avant = None, apres = None):
    return HttpResponse(status = 200)

def inscription(request):
    if(request.method == 'POST'):
        form_user = DUlSineUserCreationForm(request.POST)
        form_benevole = BenevoleForm(request.POST)
        print >>sys.stderr, form_user.errors
        print >>sys.stderr, form_benevole.errors
        if form_user.is_valid() and form_benevole.is_valid():
            user = form_user.save()
            benevole = form_benevole.save(commit = False)
            benevole.user = user
            benevole.save()
            return HttpResponseRedirect(reverse('benevole.inscription.confirmation'))
    else:
        form_user = DUlSineUserCreationForm()
        form_benevole = BenevoleForm()
    return render_to_response('benevole/inscription/nouveau.html', {'form_user' : form_user, 'form_benevole' : form_benevole}, context_instance = RequestContext(request))

def inscription_confirmation(request):
    return render_to_response('benevole/inscription/confirmation.html', context_instance = RequestContext(request))

