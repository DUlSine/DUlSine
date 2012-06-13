from django.http import HttpResponse

def index(request, delegation):
    return HttpResponse(status=200)

def details(request, delegation, id):
    return HttpResponse(status=200)

def nouveau(request, delegation, hash=None):
    return HttpResponse(status=200)

def calendrier(request, delegation, avant=None, apres=None):
    return HttpResponse(status=200)
