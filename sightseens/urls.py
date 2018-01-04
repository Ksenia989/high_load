from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # todo path(r'^post/(\d+)/$', views.getEntity, name='get_entity'),
]
