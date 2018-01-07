# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from sightseens.models import User, Visit, Location, UserSerializer, VisitSerializer, LocationSerializer


def index(request):
    return HttpResponse("Hello, world! It's my first Django project")


def getEntity(request, entity, entity_id):
    global u, data
    if request.method == 'GET':
        if entity == 'users':
            u = get_object_or_404(User, pk=entity_id)
            serializer = UserSerializer(u)
            data = getJsonData(serializer)
        elif entity == 'visits':
            u = Visit.objects.get(id=entity_id)
            serializer = VisitSerializer(u)
            data = getJsonData(serializer)
        elif entity == 'locations':
            u = Location.objects.get(id=entity_id)
            serializer = LocationSerializer(u)
            data = getJsonData(serializer)
        else:
            u = HttpResponse(status=404)
    return JsonResponse(data=data, safe=False)  # safe-False для сериализации не kv obj


def getJsonData(serializer):
    dict_user = serializer.data
    json = JSONRenderer().render(dict_user)
    stream = BytesIO(json)
    return JSONParser().parse(stream)


from django.shortcuts import render


def getPersonVisitList(request, entity_id):
    person_visit_list = Visit.objects.filter(user=entity_id)
    context = {
        'all_visits_list': person_visit_list,
        'user': User.objects.get(id=entity_id)
    }
    return render(request, 'sightseens/visit_list.html', context)


def getLocationAverageMark(request):
    return None


def updateUser(request):
    return None


def createUser(request):
    return None
