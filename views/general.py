# -*- coding: utf-8 -*-
# vim: set ts=4
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required
def index(request, delegation):
    return HttpResponse(status=200)
