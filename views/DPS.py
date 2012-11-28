# -*- coding: utf-8 -*-
# vim: set ts=4
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.forms import ModelForm, RadioSelect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from DUlSine.models import DPS, Structure, Dimensionnement, Organisateur


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
        exclude = ('hash_id', 'structure', 'organisateur', 'prix')


class DimensionnementForm(ModelForm):
    class Meta:
        model = Dimensionnement
        widgets = {
            'P2': RadioSelect,
            'E1': RadioSelect,
            'E2': RadioSelect
        }
        exclude = ('DPS', 'IS')



def index(request, structure):
    # Check that the structure does exist
    Struct = get_object_or_404(Structure, numero = structure)

    dimensionnements = Dimensionnement.objects.all()
    return render_to_response('dps/index.html', {'structure': Struct, 'all_dim': dimensionnements}, context_instance=RequestContext(request))



def details(request, structure, dim_id):
    # Check that the structure does exist
    Struct = get_object_or_404(Structure, numero = structure)
    dimensionnement = get_object_or_404(Dimensionnement, pk = dim_id)

    return render_to_response('dps/details.html', {'structure': Struct, 'dim': dimensionnement}, context_instance = RequestContext(request))



def demande(request):
    if(request.method == 'POST'):
        form_orga = OrganisateurForm(request.POST)
        form_dps = DPSForm(request.POST)
        if(form_orga.is_valid() and form_dps.is_valid()):
            orga = form_orga.save()
            dps = form_dps.save(commit=False)
#            dps.structure = Struct
            dps.organisateur = orga
            dps.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form_orga = OrganisateurForm()
        form_dps = DPSForm()
    return render_to_response('dps/demande.html', {'form_orga': form_orga, 'form_dps': form_dps}, context_instance=RequestContext(request))


def dimensionnement(request, structure, dps_hash, dim_id=None):
    # Check that the structure does exist
    Struct = get_object_or_404(Structure, numero = structure)
    dps = get_object_or_404(DPS, hash_id=dps_hash)

    # Is it a new dimensionnement ?
    if(dim_id == None):
        if(request.method == 'POST'):
            form = DimensionnementForm(request.POST)
            if(form.is_valid()):
                dim = form.save(commit = False)
                dim.DPS = dps
                dim.save()
                return HttpResponseRedirect(reverse('dps.nouveau.dimensionnement', args=[structure, dps_hash, dim.id]))
        else:
            form = DimensionnementForm()

    else:
        dim = get_object_or_404(Dimensionnement, pk=dim_id)
        form = DimensionnementForm(instance=dim)

    return render_to_response('dps/nouveau_dimensionnement.html', {'form': form}, context_instance=RequestContext(request))



def calendrier(request, structure, avant=None, apres=None):
    return HttpResponse(status=200)


def devis(request, structure, dps_id):
    Struct = get_object_or_404(Structure, numero = structure)
    dps = get_object_or_404(DPS, pk = dps_id, structure = Struct)

    return render_to_response('dps/devis.html', {'structure': Struct, 'dps': dps}, context_instance=RequestContext(request))


def admin_index(request, structure):
    return HttpResponse(status = 200)


def admin_details(request, structure, dps_id):
    return HttpResponse(status = 200)
