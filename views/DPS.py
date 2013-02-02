# -*- coding: utf-8 -*-
# vim: set ts=4
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.forms import ModelForm, RadioSelect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.contrib.auth.decorators import login_required

from DUlSine.models import DPS, Structure, Dimensionnement, Organisateur, Souhait, DIPLOME_SECOURS

import json


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


@login_required
def index(request, structure):
    # Check that the structure does exist
    Struct = get_object_or_404(Structure, numero = structure)

    # Get all the dimensionnements for that structure
    dimensionnements = Dimensionnement.objects.filter(DPS__structure = Struct)
    return render_to_response('dps/index.html', {'structure': Struct, 'all_dim': dimensionnements}, context_instance = RequestContext(request))



@login_required
def details(request, structure, dim_id):
    # Check that the structure does exist
    Struct = get_object_or_404(Structure, numero = structure)
    dimensionnement = get_object_or_404(Dimensionnement, pk = dim_id)

    return render_to_response('dps/details.html', {'structure': Struct, 'dim': dimensionnement}, context_instance = RequestContext(request))



@login_required
def inscription(request, structure, dim_id, fonction):
    # Check that the structure and dimensionnement does exists
    Struct = get_object_or_404(Structure, numero = structure)
    dimensionnement = get_object_or_404(Dimensionnement, pk = dim_id)

    # Add the wish for this user to the dimensionnement
    # TODO: check that the require formation for the function is ok

    # Check that the values are in [0: CI, 3: PSC1]
    fonction = int(fonction)
    if fonction < 0 and fonction > 3:
        raise Http404()

    # Delete the privious wish if any
    wishes = Souhait.objects.filter(benevole = request.user.benevole, dimensionnement = dimensionnement)
    for wish in wishes:
        wish.delete()

    # Create the wish
    new_wish = Souhait(benevole = request.user.benevole, dimensionnement = dimensionnement, fonction = DIPLOME_SECOURS[fonction][0])
    new_wish.save()

    return HttpResponse(json.dumps({'fonction': DIPLOME_SECOURS[fonction][1],
                                    'dim': dim_id}),
                        mimetype='application/json')



def demande(request):
    if(request.method == 'POST'):
        form_orga = OrganisateurForm(request.POST)
        form_dps = DPSForm(request.POST)
        if(form_orga.is_valid() and form_dps.is_valid()):
            orga = form_orga.save()
            dps = form_dps.save(commit = False)
            dps.organisateur = orga
            dps.save()
            return HttpResponseRedirect(reverse('dps.demande.verification', args = [dps.hash_id]))
    else:
        form_orga = OrganisateurForm()
        form_dps = DPSForm()
    return render_to_response('dps/demande/nouveau.html', {'form_orga': form_orga, 'form_dps': form_dps, 'nouveau': True}, context_instance = RequestContext(request))



def demande_details(request, dps_hash):
    dps = get_object_or_404(DPS, hash_id = dps_hash)
    dims = Dimensionnement.objects.filter(DPS = dps)
    return render_to_response('dps/demande/index.html', {'dps': dps, 'dims': dims}, context_instance = RequestContext(request))



def demande_verification(request, dps_hash):
    dps = get_object_or_404(DPS, hash_id = dps_hash)
    return render_to_response('dps/demande/resume.html', {'dps': dps }, context_instance = RequestContext(request))



def demande_modification(request, dps_hash):
    # Get the already existing DPS and corresponding Orga
    dps = get_object_or_404(DPS, hash_id = dps_hash)
    orga = get_object_or_404(Organisateur, pk = dps.organisateur.pk)

    if(request.method == 'POST'):
        # validate the data and save it
        form_orga = OrganisateurForm(request.POST, instance = orga)
        form_dps = DPSForm(request.POST, instance = dps)
        if(form_orga.is_valid() and form_dps.is_valid()):
            orga = form_orga.save()
            dps = form_dps.save()
            # redirect to the varification page
            return HttpResponseRedirect(reverse('dps.demande.verification', args = [dps.hash_id]))

    else:
        # Give default values to the forms
        form_orga = OrganisateurForm(instance = orga)
        form_dps = DPSForm(instance = dps)

    return render_to_response('dps/demande/nouveau.html', {'form_orga': form_orga, 'form_dps': form_dps, 'nouveau': False}, context_instance = RequestContext(request))



def dimensionnement(request, dps_hash, dim_id = None):
    # Check that the DPS does exist
    dps = get_object_or_404(DPS, hash_id = dps_hash)

    # Is it a new dimensionnement ?
    if(dim_id == None):
        if(request.method == 'POST'):
            form = DimensionnementForm(request.POST)
            if(form.is_valid()):
                dim = form.save(commit = False)
                dim.DPS = dps
                dim.save()
                return HttpResponseRedirect(reverse('dps.demande.dimensionnement.verification', args = [dps_hash, dim.id]))
        else:
            form = DimensionnementForm()

    else:
        dim = get_object_or_404(Dimensionnement, pk = dim_id, DPS = dps)
        form = DimensionnementForm(instance = dim)

    return render_to_response('dps/demande/dimensionnement_nouveau.html', {'form': form, 'nouveau': True}, context_instance = RequestContext(request))



def dimensionnement_verification(request, dps_hash, dim_id):
    # Check that the Dimensionnement does exist and is associated with the right DPS
    dim = get_object_or_404(Dimensionnement, pk = dim_id, DPS__hash_id = dps_hash)
    return render_to_response('dps/demande/dimensionnement_resume.html', {'dps_hash': dps_hash, 'dim': dim }, context_instance = RequestContext(request))



def dimensionnement_modification(request, dps_hash, dim_id):
    # Get the already existing DPS and corresponding Dimensionnement
    dim = get_object_or_404(Dimensionnement, pk = dim_id, DPS__hash_id = dps_hash)

    if(request.method == 'POST'):
        # validate the data and save it
        form = DimensionnementForm(request.POST, instance = dim)
        if(form.is_valid()):
            dim = form.save()
            # redirect to the verification page
            return HttpResponseRedirect(reverse('dps.demande.dimensionnement.verification', args = [dps_hash, dim.id]))

    else:
        # Give default values to the form
        form = DimensionnementForm(instance = dim)

    return render_to_response('dps/demande/dimensionnement_nouveau.html', {'form': form, 'nouveau': False}, context_instance = RequestContext(request))




def calendrier(request, structure, avant = None, apres = None):
    return HttpResponse(status = 200)



def devis(request, structure, dps_id):
    Struct = get_object_or_404(Structure, numero = structure)
    dps = get_object_or_404(DPS, pk = dps_id, structure = Struct)

    return render_to_response('dps/devis.html', {'structure': Struct, 'dps': dps}, context_instance = RequestContext(request))



def admin_index(request, structure):
    Struct = get_object_or_404(Structure, numero = structure)
    # Get all the dimensionnements for that structure
    dimensionnements = Dimensionnement.objects.filter(DPS__structure = Struct)

    return render_to_response('dps/admin/index.html',  {'structure': Struct, 'all_dim': dimensionnements}, context_instance = RequestContext(request))



def admin_details(request, structure, dps_id):
    Struct = get_object_or_404(Structure, numero = structure)
    dps = get_object_or_404(DPS, pk = dps_id)
    dimensionnements = Dimensionnement.objects.filter(DPS = dps)

    return render_to_response('dps/admin/details.html', {'structure': Struct, 'dps': dps, 'all_dim': dimensionnements}, context_instance = RequestContext(request))



def admin_dimensionnement(request, structure, dps_id, dim_id):
    Struct = get_object_or_404(Structure, numero = structure)
    dimensionnement = get_object_or_404(Dimensionnement, pk = dim_id, DPS__pk = dps_id)
    souhaits = Souhait.objects.filter(dimensionnement = dimensionnement)

    return render_to_response('dps/admin/dimensionnement.html', {'structure': Struct, 'dim': dimensionnement, 'souhaits': souhaits}, context_instance = RequestContext(request))
