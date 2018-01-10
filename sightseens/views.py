# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import Http404
from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from sightseens.models import User, Visit, Location, UserSerializer, VisitSerializer, LocationSerializer, \
    ShortVisitSerializer, PlaceSerializer


def index(request):
    return HttpResponse("Hello, world! It's my first Django project")


# todo переименовать всё в pythonic style
def getEntity(request, entity, entity_id):
    global u, data
    if request.method == 'GET':
        if entity == 'users':
            u = get_object_or_404(User, pk=entity_id)
            serializer = UserSerializer(u)
            data = get_json_data(serializer)
        elif entity == 'visits':
            u = Visit.objects.get(id=entity_id)
            serializer = VisitSerializer(u)
            data = get_json_data(serializer)
        elif entity == 'locations':
            u = Location.objects.get(id=entity_id)
            serializer = LocationSerializer(u)
            data = get_json_data(serializer)
        else:
            u = HttpResponse(status=404)
    return JsonResponse(data=data, safe=False)


def validateListViaRequest(visit_list, dict):
    FROM_DATE = 'fromDate'
    TO_DATE = 'toDate'
    COUNTRY = 'country'
    TO_DISTANCE = 'toDistance'

    if FROM_DATE in dict.keys():
        res_list = []
        from_date = dict.get(FROM_DATE)
        check_int(from_date)

        for el in visit_list:
            # эта ужастная конструкция преобразует datetime в timestamp в строке (чтобы сравнить в фронтом)
            # а каст к инту, т.к. возвращается float (хз, почему)
            if int(el.visited_at.timestamp()) > int(float(from_date)):
                res_list.append(el)
                visit_list = res_list
    if TO_DATE in dict.keys():
        to_date = dict.get(TO_DATE)
        check_int(to_date)
        res_list = []
        for el in visit_list:
            if int(el.visited_at.timestamp()) < int(float(to_date)):
                res_list.append(el)
        visit_list = res_list
    if COUNTRY in dict.keys():
        country = dict.get(COUNTRY)
        res_list = []
        for el in visit_list:
            visit_location = Location.objects.get(pk=el.location.id)
            if visit_location.country == country:
                res_list.append(el)
        visit_list = res_list
    if TO_DISTANCE in dict.keys():
        to_distance = dict.get(TO_DISTANCE)
        check_int(to_distance)
        res_list = []
        for el in visit_list:
            visit_location = Location.objects.get(pk=el.location.id)
            if visit_location.distance < int(float(to_distance)):
                res_list.append(el)
        visit_list = res_list

    return visit_list


def check_int(from_date):
    try:
        int(float(from_date))
    except ValueError:
        raise Http404()


def getPersonVisitList(request, entity_id):
    user_visits = get_list_or_404(Visit, user=entity_id)
    my_list = []
    # проверка списка и его сокращение в соответствии с GET - запросом
    user_visits = validateListViaRequest(user_visits, request.GET)
    for visit in user_visits:
        serializer = ShortVisitSerializer(visit)
        full_data = get_json_data(serializer)
        # для каждого visit получаем дополнительное поле с описанием
        location_description = get_object_or_404(Location, id=visit.location.id)
        location_description_serializer = PlaceSerializer(location_description)
        ld = get_json_data(location_description_serializer)
        full_data['place'] = ld.get('place')
        my_list.append(full_data)

    #     оборачиваем в visits
    new_dict= {'visits': my_list}
    return JsonResponse(new_dict, safe=False)


def getLocationAverageMark(request):
    return None


def updateUser(request):
    return None


def createUser(request):
    return None


def get_json_data(serializer):
    dict_user = serializer.data
    json = JSONRenderer().render(dict_user)
    stream = BytesIO(json)
    return JSONParser().parse(stream)
