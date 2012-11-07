# -*- coding: utf-8 -*-
# vim: set ts=4
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.forms import ModelForm, RadioSelect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from DUlSine.models import DPS, Delegation, Dimensionnement, Organisateur


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


class DimensionnementForm(ModelForm):
    class Meta:
        model = Dimensionnement
        widgets = {
            'P2': RadioSelect,
            'E1': RadioSelect,
            'E2': RadioSelect
        }
        exclude = ('DPS', 'IS')



def index(request, delegation):
    # Check that the DL does exist
    DL = get_object_or_404(Delegation, numero=delegation)

    dimensionnements = Dimensionnement.objects.all()
    return render_to_response('dps/index.html', {'DL': DL, 'all_dim': dimensionnements})



def details(request, delegation, dps_id):
    return HttpResponse(status=200)



def demande(request):
    if(request.method == 'POST'):
        form_orga = OrganisateurForm(request.POST)
        form_dps = DPSForm(request.POST)
        if(form_orga.is_valid() and form_dps.is_valid()):
            orga = form_orga.save()
            dps = form_dps.save(commit=False)
            dps.delegation = DL
            dps.organisateur = orga
            dps.save()
            return HttpResponseRedirect(reverse('general.index'))
    else:
        form_orga = OrganisateurForm()
        form_dps = DPSForm()
    return render_to_response('dps/demande.html', {'form_orga': form_orga, 'form_dps': form_dps}, context_instance=RequestContext(request))


def dimensionnement(request, delegation, dps_hash, dim_id=None):
    # Check that the DL does exist
    DL = get_object_or_404(Delegation, numero=delegation)
    dps = get_object_or_404(DPS, hash_id=dps_hash)

    # Is it a new dimensionnement ?
    if(dim_id == None):
        if(request.method == 'POST'):
            form = DimensionnementForm(request.POST)
            if(form.is_valid()):
                dim = form.save(commit = False)
                dim.DPS = dps
                dim.save()
                return HttpResponseRedirect(reverse('dps.nouveau.dimensionnement', args=[delegation, dps_hash, dim.id]))
        else:
            form = DimensionnementForm()

    else:
        dim = get_object_or_404(Dimensionnement, pk=dim_id)
        form = DimensionnementForm(instance=dim)

    return render_to_response('dps/nouveau_dimensionnement.html', {'form': form}, context_instance=RequestContext(request))



def calendrier(request, delegation, avant=None, apres=None):
    return HttpResponse(status=200)


def devis(request, delegation, dps_id):
    DL = get_object_or_404(Delegation, numero = delegation)
    dps = get_object_or_404(DPS, pk = dps_id, delegation = DL)

    return render_to_response('dps/devis.html', {'DL': DL, 'dps': dps})


def admin_index(request, delegation):
    return HttpResponse(status = 200)


def admin_details(request, delegation, dps_id):
    return HttpResponse(status = 200)
