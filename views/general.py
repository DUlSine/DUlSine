# -*- coding: utf-8 -*-
# vim: set ts=4
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext


def index(request):
    return render_to_response('general/index.html', context_instance=RequestContext(request))
