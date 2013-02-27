# -*- coding: utf-8 -*-
# vim: set ts=4

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from DUlSine.models import Structure, Benevole

import sys


class BenevoleForm(ModelForm):
    class Meta:
        model = Benevole
        exclude = ("user",)

    def __init__(self, *args, **kwargs):
        super(BenevoleForm, self).__init__(*args, **kwargs)
        # Add HTML5 attributes
        self.fields['date_naissance'].widget.attrs['placeholder'] = 'jj/mm/aaaa'
        self.fields['telephone'].widget.attrs['placeholder'] = '06.00.00.00.00'



class DUlSineUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", \
                  "username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(DUlSineUserCreationForm, self).__init__(*args, **kwargs)
        # Add HTML5 attributes
        self.fields['username'].widget.attrs['autofocus'] = 'autofocus'
        self.fields['email'].widget.attrs['placeholder'] = '@example.com'


@login_required
def index(request, structure):
    Struct = get_object_or_404(Structure, numero = structure)
    benevoles = Benevole.objects.filter(structure = structure)

    return render_to_response('benevole/index.html', {'structure': Struct, 'benevoles': benevoles}, context_instance = RequestContext(request))



@login_required
def details(request, benevole_id):
    benevole = get_object_or_404(Benevole, id = benevole_id)

    # Find previous and next benevoles
    benevoles = Benevole.objects.filter(structure = benevole.structure)
    previous_b = 0
    next_b = 0
    index = 0
    for b in benevoles:
        index = index + 1
        if b.pk == int(benevole_id):
            if index < benevoles.count():
                next_b = benevoles[index].pk
            break
        previous_b = b.pk

    return render_to_response('benevole/details.html', {'benevole': benevole, 'previous': previous_b, 'next': next_b}, context_instance = RequestContext(request))



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


@login_required
def moncompte(request):
    return render_to_response('benevole/moncompte.html', context_instance = RequestContext(request))
