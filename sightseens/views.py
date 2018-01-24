# Create your views here.
import calendar
from datetime import datetime
import datetime

from dateutil.relativedelta import relativedelta
from django.db import IntegrityError
from django.http import Http404
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils.six import BytesIO
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from sightseens.models.Location import Location, LocationSerializer
from sightseens.models.User import UserSerializer, User
from sightseens.models.Visit import Visit, VisitSerializer, ShortVisitSerializer, PlaceSerializer


def index(request):
    return HttpResponse("Hello, world! It's my first Django project")


#todo
def update_visit(oldVisit, data):
    isCorrenct = right_or_404(data)
    if isCorrenct:
        if 'location' in data:
            l=Location.objects.filter(pk=data['location'])
            oldVisit.location = l
        if 'user' in data:
            u=User.objects.filter(pk=data['user'])
            oldVisit.user = u


        if 'mark' in data:
            oldVisit.mark = data['mark']
        if 'visited_at' in data:
            oldVisit.visited_at = datetime.datetime.fromtimestamp(
                int(data['visited_at']))
    else:
        return isCorrenct
    oldVisit.save()


def update_location(oldLocation, data):
    isCorrenct = right_or_404(data)
    if isCorrenct:
        if 'place' in data:
            oldLocation.place = data['place']
        if 'country' in data:
            oldLocation.country = data['country']
        if 'city' in data:
            oldLocation.city = data['city']
        if 'distance' in data:
            oldLocation.distance = data['distance']
    else:
        return isCorrenct
    oldLocation.save()


@csrf_exempt
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
            u = Http404()
    if request.method == 'POST':
        if entity == 'users':
            oldUser = get_object_or_404(User, pk=entity_id)
            stream = BytesIO(request.body)
            data = JSONParser().parse(stream)
            updateUser(oldUser, data)
            data = {}
        elif entity == 'visits':
            oldVisit = get_object_or_404(User, pk=entity_id)
            stream = BytesIO(request.body)
            data = JSONParser().parse(stream)
            update_visit(oldVisit, data)
            data = {}
        elif entity == 'locations':
            oldLocation = get_object_or_404(User, pk=entity_id)
            stream = BytesIO(request.body)
            data = JSONParser().parse(stream)
            update_location(oldLocation, data)
            data = {}
        else:
            u = Http404()

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

    # оборачиваем в visits
    new_dict = {'visits': my_list}
    return JsonResponse(new_dict, safe=False)


def select_visits(visits_for_location, dict):
    FROM_DATE = 'fromDate'
    TO_DATE = 'toDate'
    FROM_AGE = 'fromAge'
    TO_AGE = 'toAge'
    GENDER = 'gender'

    if FROM_DATE in dict.keys():
        res_list = []
        from_date = dict.get(FROM_DATE)
        check_int(from_date)
        for el in visits_for_location:
            # эта ужастная конструкция преобразует datetime в timestamp в строке (чтобы сравнить в фронтом)
            # а каст к инту, т.к. возвращается float (хз, почему)
            if int(el.visited_at.timestamp()) > int(float(from_date)):
                res_list.append(el)
                visits_for_location = res_list
    if TO_DATE in dict.keys():
        to_date = dict.get(TO_DATE)
        check_int(to_date)
        res_list = []
        for el in visits_for_location:
            if int(el.visited_at.timestamp()) < int(float(to_date)):
                res_list.append(el)
        visits_for_location = res_list
    if FROM_AGE in dict.keys():
        from_age = dict.get(FROM_AGE)
        res_list = []
        check_int(from_age)
        now = datetime.now() + relativedelta(years=int(from_age))
        timestamp = calendar.timegm(now.timetuple())
        for el in visits_for_location:
            user = User.objects.get(pk=el.user.id)
            if int(user.birth_date.timestamp()) > timestamp:
                res_list.append(el)
        visits_for_location = res_list
    if TO_AGE in dict.keys():
        to_age = dict.get(TO_AGE)
        check_int(to_age)
        res_list = []
        now = datetime.now() + relativedelta(years=int(to_age))
        timestamp = calendar.timegm(now.timetuple())
        for el in visits_for_location:
            user = User.objects.get(pk=el.user.id)
            if int(user.birth_date.timestamp()) < timestamp:
                res_list.append(el)
        visits_for_location = res_list
    if GENDER in dict.keys():
        gender = dict.get(GENDER)
        res_list = []
        for el in visits_for_location:
            user = User.objects.get(pk=el.user.id)
            if user.gender == gender:
                res_list.append(el)
        visits_for_location = res_list

    return visits_for_location


def getLocationAverageMark(request, entity_id):
    sum = 0
    visits_for_location = get_list_or_404(Visit, location=entity_id)
    visits_for_location = select_visits(visits_for_location, request.GET)
    for visit in visits_for_location:
        sum = sum + visit.mark
    average = 0
    if len(visits_for_location) != 0:
        average = sum / len(visits_for_location)
    average = round(average, 5)
    dict1 = {'avg': average}
    return JsonResponse(dict1)


def right_or_404(dataDictionary):
    for field in dataDictionary:
        if field == None:
            return HttpResponseBadRequest()
    return True

def updateUser(oldUser, dataDictionary):
    isCorrenct = right_or_404(dataDictionary)
    if isCorrenct:
        if 'email' in dataDictionary:
            oldUser.email = dataDictionary['email']
        if 'first_name' in dataDictionary:
            oldUser.first_name = dataDictionary['first_name']
        if 'last_name' in dataDictionary:
            oldUser.last_name = dataDictionary['last_name']
        if 'gender' in dataDictionary:
            oldUser.gender = dataDictionary['gender']
        if 'birth_date' in dataDictionary:
            oldUser.birth_date = datetime.datetime.fromtimestamp(
                int(dataDictionary['birth_date'])
            )
    else:
        return isCorrenct
    oldUser.save()


@csrf_exempt
def create_entity(request, entity):
    global u
    if request.method == 'POST':
        if entity == 'users':
            stream = BytesIO(request.body)
            data = JSONParser().parse(stream)
            serializer = UserSerializer(data=data)
            u = save_json_or_bad_request(serializer, clazz=User)
        elif entity == 'visits':
            stream = BytesIO(request.body)
            data = JSONParser().parse(stream)
            serializer = VisitSerializer(data=data)
            u = save_json_or_bad_request(serializer, Visit)
        elif entity == 'locations':
            stream = BytesIO(request.body)
            data = JSONParser().parse(stream)
            serializer = LocationSerializer(data=data)
            u = save_json_or_bad_request(serializer, Location)
        else:
            u = Http404()
    return HttpResponse(u.content, status=u.status_code)


def save_json_or_bad_request(serializer, clazz):
    try:
        if serializer.is_valid(raise_exception=True):
            if clazz == Visit:
                obj2 = serializer.create(serializer.initial_data)
                obj2.save()
            else:
                obj2 = clazz.objects.create(**serializer.validated_data)
                obj2.save()

    except ValidationError as error:
        return HttpResponseBadRequest()
    except IntegrityError as error:
        return HttpResponseBadRequest()
    return HttpResponse("{}", status=200)


def get_json_data(serializer):
    dict_user = serializer.data
    json = JSONRenderer().render(dict_user)
    stream = BytesIO(json)
    return JSONParser().parse(stream)


def check_int(from_date):
    try:
        int(float(from_date))
    except ValueError:
        raise Http404()
