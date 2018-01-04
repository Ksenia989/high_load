from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world! It's my first Django project")


def getEntity(request):
    # todo сделать выборку из таблички
    return None