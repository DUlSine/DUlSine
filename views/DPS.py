# -*- coding: utf-8 -*-
# vim: set ts=4
from django.core.urlresolvers import reverse
from django.forms import ModelForm, RadioSelect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from DUlSine.models import DPS, Delegation, Organisateur


class OrganisateurForm(ModelForm):
    class Meta:
        model = Organisateur
        widgets = {
            'contact_civilite': RadioSelect,
            'representant_civilite': RadioSelect
        }



class DPSForm(ModelForm):
    class Meta:
        model = DPS
        widgets = {
            'contact_sur_place_civilite': RadioSelect
        }
        exclude = ('hash_id', 'delegation', 'organisateur', 'prix')



def index(request, delegation):
    return HttpResponse(status=200)



def details(request, delegation, dps_id):
    return HttpResponse(status=200)



def nouveau(request, delegation, dps_hash=None):
    # Vérifie le numéro de délégation
    DL = get_object_or_404(Delegation, numero=delegation)

    # Est-ce une nouvelle demande pour un DPS
    if(dps_hash == None):
        if(request.method == 'POST'):
            form_orga = OrganisateurForm(request.POST)
            form_dps = DPSForm(request.POST)
            if(form_orga.is_valid() and form_dps.is_valid()):
                orga = form_orga.save()
                dps = form_dps.save(commit=False)
                dps.delegation = DL
                dps.organisateur = orga
                dps.save()
                return HttpResponseRedirect(reverse('dps.nouveau.dimenssionnement', args=[delegation, dps.hash_id, 0]))
        else:
            form_orga = OrganisateurForm()
            form_dps = DPSForm()
        return render_to_response('dps/nouveau.html', {'form_orga': form_orga, 'form_dps': form_dps}, context_instance=RequestContext(request))


def dimenssionnement(request, delegation, dps_hash, dim_id=None):
    return HttpResponse(status=200)


def calendrier(request, delegation, avant=None, apres=None):
    return HttpResponse(status=200)
