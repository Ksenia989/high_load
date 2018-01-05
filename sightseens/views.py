from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from sightseens.models import User, Visit, Location


def index(request):
    return HttpResponse("Hello, world! It's my first Django project")


def getEntity(request, entity, entity_id):
    global u
    if request.method == 'GET':
        if entity == 'users':
            try:
                u = User.objects.get(id=entity_id)
            except Exception:
                u = HttpResponse(status=404)
        elif entity == 'visits':
            u = Visit.objects.get(id=entity_id)
        elif entity == 'locations':
            u = Location.objects.get(id=entity_id)
        else:
            u = HttpResponse(status=404)
    return HttpResponse(u)


from django.template import loader

def getPersonVisitList(request, entity_id):
    person_visit_list=Visit.objects.filter(user=entity_id)
    template = loader.get_template('sightseens/visit_list.html')
    context = {
        'all_visits_list': person_visit_list,
        'user': User.objects.get(id=entity_id)
    }
    return HttpResponse(template.render(context, request))


def getLocationAverageMark(request):
    return None


def updateUser(request):
    return None


def createUser(request):
    return None
