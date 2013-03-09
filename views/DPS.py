# -*- coding: utf-8 -*-
# vim: set ts=4

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms import ModelForm, RadioSelect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext


from DUlSine.models import Dimensionnement, DPS, Inscription, Organisateur, Structure, Team, Wish
from DUlSine.models.dulsine_commons import *

import json


class OrganisateurForm(ModelForm):
    class Meta:
        model = Organisateur
        widgets = {
            'contact_civilite': RadioSelect,
            'representant_civilite': RadioSelect
        }
    def __init__(self, *args, **kwargs):
        super(OrganisateurForm, self).__init__(*args, **kwargs)
        # Add HTML5 attributes
        self.fields['contact_civilite'].widget.attrs['autofocus'] = 'autofocus'
        self.fields['contact_fonction'].widget.attrs['placeholder'] = 'président, trésorier, ...'
        self.fields['representant_fonction'].widget.attrs['placeholder'] = 'président, trésorier, ...'



class DPSForm(ModelForm):
    class Meta:
        model = DPS
        widgets = {
            'contact_sur_place_civilite': RadioSelect
        }
        exclude = ('hash_id', 'structure', 'organisateur', 'prix')

    def __init__(self, *args, **kwargs):
        super(DPSForm, self).__init__(*args, **kwargs)
        # Add HTML5 attributes
        self.fields['objet'].widget.attrs['placeholder'] = 'concert, spectacle, repas, ...'



class DimensionnementForm(ModelForm):
    class Meta:
        model = Dimensionnement
        widgets = {
            'P2': RadioSelect,
            'E1': RadioSelect,
            'E2': RadioSelect
        }
        exclude = ('DPS', 'IS')

    def __init__(self, *args, **kwargs):
        super(DimensionnementForm, self).__init__(*args, **kwargs)
        # Add HTML5 attributes
        self.fields['nom'].widget.attrs['autofocus'] = 'autofocus'
        self.fields['debut'].widget.attrs['placeholder'] = 'jj/mm/aaaa hh:mm'
        self.fields['fin'].widget.attrs['placeholder'] = 'jj/mm/aaaa hh:mm'
        self.fields['besoins_specifiques'].widget.attrs['placeholder'] = 'aucun'



@login_required
def index(request, structure):
    # Check that the structure does exist
    Struct = get_object_or_404(Structure, numero = structure)

    # Get all the dimensionnements for that structure
    dimensionnements = Dimensionnement.objects.filter(DPS__structure = Struct)
    return render_to_response('dps/index.html', {'structure': Struct, 'all_dim': dimensionnements, 'DIPLOME_CI': DIPLOME_CI, 'DIPLOME_PSE2': DIPLOME_PSE2, 'DIPLOME_PSE1': DIPLOME_PSE1, 'DIPLOME_PSC1': DIPLOME_PSC1}, context_instance = RequestContext(request))



@login_required
def details(request, structure, dim_id):
    # Check that the structure does exist
    Struct = get_object_or_404(Structure, numero = structure)
    # TODO: add the possibility to share DPS between structures
    dimensionnement = get_object_or_404(Dimensionnement, pk = dim_id, DPS__structure = Struct)

    # Check if the user has a wish or is already subscribed
    subscription = Inscription.objects.filter(benevole = request.user, team__dimensionnement = dimensionnement)
    if subscription.count() == 1:
        fonction = subscription[0].get_fonction_display()
        wish = None
    else:
        fonction = None
        wish = Wish.objects.filter(benevole = request.user, dimensionnement = dimensionnement)
        if wish.count() == 1:
            wish = wish[0]

    return render_to_response('dps/details.html', {'structure': Struct, 'dim': dimensionnement, 'fonction': fonction, 'wish': wish}, context_instance = RequestContext(request))



@login_required
def inscription(request, structure, dim_id, wish_num):
    # Check that the structure and dimensionnement does exists
    Struct = get_object_or_404(Structure, numero = structure)
    dimensionnement = get_object_or_404(Dimensionnement, pk = dim_id)

    # Add the wish for this user to the dimensionnement
    # TODO: check that the require formation for the function is ok
    # For instance not < 18 or PSC1 inside VPSP or Binomes

    # Check that the values are in WISH_CHOICES
    wish_num = int(wish_num)
    if (wish_num < 0 or wish_num > len(WISH_CHOICES)):
        raise Http404()

    # Check that the admin does not subscribe the user (not removable y the user)
    if Inscription.objects.filter(benevole = request.user.benevole, team__dimensionnement = dimensionnement).count() > 0:
        raise Http404()

    # Delete the privious wish if any
    wishes = Wish.objects.filter(benevole = request.user.benevole, dimensionnement = dimensionnement)
    for wish in wishes:
        wish.delete()

    # Create the wish
    new_wish = Wish(benevole = request.user.benevole, dimensionnement = dimensionnement, wish = wish_num)
    new_wish.save()

    return HttpResponse(json.dumps({'wish': new_wish.get_wish_display(),
                                    'dim': dim_id,
                                    'nombreND': dimensionnement.nombreND()}),
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



def demande_envoyer(request, dps_hash):
    dps = get_object_or_404(DPS, hash_id = dps_hash)

    # Test that we have at least 1 dimensionnement
    if(Dimensionnement.objects.filter(DPS = dps).count() == 0):
        return HttpResponseRedirect(reverse('dps.demande.details', args = [dps_hash]))

    # TODO: to implement completely
    raise Http404



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

    return render_to_response('dps/demande/nouveau.html', {'form_orga': form_orga, 'form_dps': form_dps, 'dps': dps, 'nouveau': False}, context_instance = RequestContext(request))



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

    return render_to_response('dps/demande/dimensionnement_nouveau.html', {'form': form, 'dps': dps, 'nouveau': True}, context_instance = RequestContext(request))



def dimensionnement_verification(request, dps_hash, dim_id):
    # Check that the Dimensionnement does exist and is associated with the right DPS
    dim = get_object_or_404(Dimensionnement, pk = dim_id, DPS__hash_id = dps_hash)
    return render_to_response('dps/demande/dimensionnement_resume.html', {'dps': dim.DPS, 'dim': dim }, context_instance = RequestContext(request))



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

    return render_to_response('dps/demande/dimensionnement_nouveau.html', {'form': form, 'dps': dim.DPS, 'nouveau': False}, context_instance = RequestContext(request))



def dimensionnement_copy(request, dps_hash, dim_id):
    # Get the already existing DPS and corresponding Dimensionnement
    dim = get_object_or_404(Dimensionnement, pk = dim_id, DPS__hash_id = dps_hash)

    # Change the values to not override the name
    dim.nom = dim.nom + ' (copie)'
    # Remove the primary key: this is now a new object
    setattr(dim, 'pk', None)
    dim.save()

    return HttpResponseRedirect(reverse('dps.demande.details', args = [dps_hash]))



def dimensionnement_delete(request, dps_hash, dim_id):
    # Get the already existing DPS and corresponding Dimensionnement
    dim = get_object_or_404(Dimensionnement, pk = dim_id, DPS__hash_id = dps_hash)
    dim.delete()

    return HttpResponseRedirect(reverse('dps.demande.details', args = [ dps_hash]))



def calendrier(request, structure, avant = None, apres = None):
    return HttpResponse(status = 200)



def devis(request, structure, dps_id):
    Struct = get_object_or_404(Structure, numero = structure)
    dps = get_object_or_404(DPS, pk = dps_id, structure = Struct)

    return render_to_response('dps/devis.html', {'structure': Struct, 'dps': dps}, context_instance = RequestContext(request))



@login_required
def admin_index(request, structure):
    Struct = get_object_or_404(Structure, numero = structure)
    # Get all the dimensionnements for that structure
    dimensionnements = Dimensionnement.objects.filter(DPS__structure = Struct)

    return render_to_response('dps/admin/index.html',  {'structure': Struct, 'all_dim': dimensionnements, 'DIPLOME_CI': DIPLOME_CI, 'DIPLOME_PSE2': DIPLOME_PSE2, 'DIPLOME_PSE1': DIPLOME_PSE1, 'DIPLOME_PSC1': DIPLOME_PSC1}, context_instance = RequestContext(request))



@login_required
def admin_details(request, structure, dps_id):
    Struct = get_object_or_404(Structure, numero = structure)
    dps = get_object_or_404(DPS, pk = dps_id)
    dimensionnements = Dimensionnement.objects.filter(DPS = dps)

    return render_to_response('dps/admin/details.html', {'structure': Struct, 'dps': dps, 'all_dim': dimensionnements, 'DIPLOME_CI': DIPLOME_CI, 'DIPLOME_PSE2': DIPLOME_PSE2, 'DIPLOME_PSE1': DIPLOME_PSE1, 'DIPLOME_PSC1': DIPLOME_PSC1}, context_instance = RequestContext(request))



@login_required
def admin_dimensionnement(request, structure, dps_id, dim_id):
    Struct = get_object_or_404(Structure, numero = structure)
    dimensionnement = get_object_or_404(Dimensionnement, pk = dim_id, DPS__pk = dps_id)
    wishes = Wish.objects.filter(dimensionnement = dimensionnement).filter(~Q(wish = WISH_ND))
    not_available = Wish.objects.filter(dimensionnement = dimensionnement, wish = WISH_ND)
    teams = Team.objects.filter(dimensionnement = dimensionnement)

    return render_to_response('dps/admin/dimensionnement.html', {'structure': Struct, 'dim': dimensionnement, 'teams': teams, 'wishes': wishes, 'not_available': not_available}, context_instance = RequestContext(request))
