from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(r'^(\d+)/(\d+)$', views.getEntity, name='get_entity'),
    path(r'^users/(\d+)/visits$', views.getPersonVisitList, name='get_visit_list_for_person'),
    path(r'^location/(\d+)/avg', views.getLocationAverageMark, name='get_average_mark_for_location'),
    path(r'^(\d+)/(\d+)$', views.updateUser, name='update_user'),  # entity, id
    path(r'^(\d+)/new$', views.createUser, name='new_user'),  # user
]
