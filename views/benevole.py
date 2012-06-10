from django.http import HttpResponse

def index(request, delegation):
    return HttpResponse(status=200)

def details(request, id):
    return HttpResponse(status=200)

def calendrier(request, id, type=None, avant=None, apres=None):
    return HttpResponse(status=200)
